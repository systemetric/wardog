#include <sys/epoll.h>
#include <sys/stat.h>

#include "wardog/daemon/daemon.hpp"
#include "wardog/daemon/util.hpp"

namespace wardog
{

WardogDaemon::WardogDaemon(std::filesystem::path sock_path, Logger &logger,
                           unsigned int sock_gid)
    : m_sock_path(sock_path), m_logger(logger), m_sock_gid(sock_gid)
{
    umask(S_IROTH | S_IWOTH);

    if ((m_epoll_fd = epoll_create1(0)) < 0)
        throw_errno("epoll_create1");
}

WardogDaemon::~WardogDaemon() { close(m_epoll_fd); }

int
WardogDaemon::run()
{
    m_logger.info("hello from wardog!");
    return 0;
}

}; // namespace wardog
