#ifndef daemon_hpp_INCLUDED
#define daemon_hpp_INCLUDED

#include <filesystem>

#include "wardog/daemon/logging.hpp"

namespace wardog
{

class WardogDaemon
{
private:
    int m_epoll_fd = -1;

    std::filesystem::path m_sock_path;
    Logger &m_logger;
    unsigned int m_sock_gid;

public:
    WardogDaemon(std::filesystem::path path, Logger &logger,
                 unsigned int sock_gid);
    ~WardogDaemon();

    int run();
};

}; // namespace wardog

#endif // daemon_hpp_INCLUDED
