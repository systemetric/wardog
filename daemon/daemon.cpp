#include <cerrno>
#include <cstring>
#include <fcntl.h>
#include <memory>
#include <stdexcept>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/un.h>
#include <unistd.h>

#include "wardog/daemon/client.hpp"
#include "wardog/daemon/daemon.hpp"
#include "wardog/daemon/util.hpp"

namespace wardog
{

WardogDaemon::WardogDaemon(std::filesystem::path sock_path, Logger &logger,
                           unsigned int sock_gid)
    : m_sock_path(sock_path), m_logger(logger), m_sock_gid(sock_gid)
{
    umask(S_IROTH | S_IWOTH);

    if (std::strlen(sock_path.c_str()) > sizeof(m_sock_addr.sun_path) - 1)
        throw std::runtime_error(
            "Socket path too long for 'm_sock_addr.sun_path'");

    m_sock_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (m_sock_fd == -1)
        throw_errno("socket");

    // set non-blocking mode on this file descriptor
    int flags = fcntl(m_sock_fd, F_GETFL);
    if (flags == -1)
        throw_errno("fcntl F_GETFL");
    if (fcntl(m_sock_fd, F_SETFL, flags | O_NONBLOCK) == -1)
        throw_errno("fcntl F_SETFL");

    if (unlink(sock_path.c_str()) && errno != ENOENT)
        throw_errno("unlink");

    m_sock_addr.sun_family = AF_UNIX;
    std::strncpy(m_sock_addr.sun_path, sock_path.c_str(),
                 sizeof(m_sock_addr.sun_path) - 1);
    m_sock_addr.sun_path[sizeof(m_sock_addr.sun_path) - 1] = '\0';

    if (bind(m_sock_fd, (struct sockaddr *)&m_sock_addr,
             sizeof(struct sockaddr_un)) == -1)
        throw_errno("bind");

    // ensure the specified group has access
    if (chown(sock_path.c_str(), getuid(), sock_gid) == -1)
        throw_errno("chown");

    if (listen(m_sock_fd, 32) == -1)
        throw_errno("listen");

    if ((m_epoll_fd = epoll_create1(0)) < 0)
        throw_errno("epoll_create1");

    m_sock_id = next_event_id();
    if (m_sock_id == 0)
        throw std::runtime_error("Out of event IDs when creating socket event");

    struct epoll_event sock_ev = {
        .events = EPOLLIN,
        .data =
            {
                .u64 = m_sock_id,
            },
    };

    if (epoll_ctl(m_epoll_fd, EPOLL_CTL_ADD, m_sock_fd, &sock_ev) == -1)
        throw_errno("epoll_ctl ADD");
}

WardogDaemon::~WardogDaemon()
{
    for (const auto &[_, client] : m_clients)
        delete client;

    close(m_epoll_fd);
    close(m_sock_fd);
    unlink(m_sock_path.c_str());
}

WardogClient *
WardogDaemon::create_client(int fd)
{
    uint64_t id = next_event_id();
    if (id == 0) {
        m_logger.warn("Failed to create client. Out of event IDs?");
        return nullptr;
    }

    WardogClient *client = new WardogClient(fd, id, m_rq_queue, m_logger);
    m_clients[id] = client;

    return client;
}

void
WardogDaemon::delete_client(uint64_t id)
{
    if (!m_clients.contains(id))
        return;

    WardogClient *client = m_clients[id];

    int fd = client->fd();
    if (epoll_ctl(m_epoll_fd, EPOLL_CTL_DEL, fd, NULL) == -1)
        throw_errno("epoll_ctl DEL");

    delete client;
    m_clients.erase(id);
}

void
WardogDaemon::handle_sock_ev()
{
    int fd;

    // accept as many connections as possible
    // ..this fd has O_NONBLOCK set
    while ((fd = accept(m_sock_fd, NULL, NULL)) != -1) {
        // set O_NONBLOCK on this fd
        int flags = fcntl(fd, F_GETFL);
        if (flags == -1)
            throw_errno("fcntl F_GETFL");
        if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) == -1)
            throw_errno("fcntl F_SETFL");

        WardogClient *client = create_client(fd);
        if (client == nullptr) {
            close(fd);
            continue;
        }

        struct epoll_event client_ev = {
            .events = EPOLLIN,
            .data =
                {
                    .u64 = client->id(),
                },
        };

        if (epoll_ctl(m_epoll_fd, EPOLL_CTL_ADD, fd, &client_ev) == -1)
            throw_errno("epoll_ctl ADD");
    }

    if (errno == EAGAIN || errno == EWOULDBLOCK)
        return;
    throw_errno("accept");
}

void
WardogDaemon::process_requests()
{
    while (!m_rq_queue.empty()) {
        WardogRequest req = m_rq_queue.front();
        m_logger.debug("REQUEST client=", req.client_id, ",mode=", req.mode,
                       ",nargs=", req.args.size());
        m_rq_queue.pop();
    }
}

void
WardogDaemon::process_events(struct epoll_event *events, int n_events)
{
    for (int i = 0; i < n_events; i++) {
        struct epoll_event *ev = &events[i];
        uint64_t ev_id = ev->data.u64;

        if (ev_id == m_sock_id) {
            if (ev->events & EPOLLIN)
                handle_sock_ev();
            if (ev->events & EPOLLHUP || ev->events & EPOLLERR)
                throw std::runtime_error(
                    "failed to poll socket file descriptor");
            continue;
        }

        if (!m_clients.contains(ev_id)) {
            m_logger.warn("Unknown client ID: ", ev_id);
            continue;
        }

        WardogClient *client = m_clients[ev_id];
        if (ev->events & EPOLLIN) {
            // slightly hacky, but that's an EOF, disconnect
            if (client->handle_ev() == 0)
                ev->events |= EPOLLHUP;
        }

        // probably the client disappeared, disconnect it
        if (ev->events & EPOLLHUP || ev->events & EPOLLERR)
            delete_client(ev_id);
    }
}

int
WardogDaemon::run()
{
    int res = 0;

    std::unique_ptr<struct epoll_event[]> events(
        new struct epoll_event[m_max_events]);

    while (res == 0) {
        int n = epoll_wait(m_epoll_fd, events.get(), m_max_events, -1);
        if (n == -1) {
            if (errno == EINTR)
                continue;

            throw_errno("epoll_wait");
            return -1;
        }

        process_events(events.get(), n);
        process_requests();
    }

    return res;
}

}; // namespace wardog
