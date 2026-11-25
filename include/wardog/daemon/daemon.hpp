#ifndef daemon_hpp_INCLUDED
#define daemon_hpp_INCLUDED

#include <cstdint>
#include <filesystem>
#include <queue>
#include <sys/un.h>
#include <unordered_map>

#include "wardog/daemon/client.hpp"
#include "wardog/daemon/logging.hpp"
#include "wardog/daemon/types.hpp"

namespace wardog
{

class WardogDaemon
{
private:
    std::unordered_map<uint64_t, WardogClient *> m_clients;
    std::queue<WardogRequest> m_rq_queue;

    uint64_t m_last_event_id = 1;
    uint64_t
    next_event_id()
    {
        if (m_last_event_id >= UINT64_MAX)
            return 0;
        return m_last_event_id++;
    }

    int m_epoll_fd = -1;
    int m_sock_fd = -1;
    uint64_t m_sock_id = 0;

    int m_max_events = 32;

    std::filesystem::path m_sock_path;
    Logger &m_logger;
    unsigned int m_sock_gid;

    struct sockaddr_un m_sock_addr;

    void handle_sock_ev();
    void process_requests();
    void process_events(struct epoll_event *events, int n_events);

    WardogClient *create_client(int fd);
    void delete_client(uint64_t id);

public:
    WardogDaemon(std::filesystem::path path, Logger &logger,
                 unsigned int sock_gid);
    ~WardogDaemon();

    int run();
};

}; // namespace wardog

#endif // daemon_hpp_INCLUDED
