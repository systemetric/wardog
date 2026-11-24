#include <cerrno>
#include <climits>
#include <iostream>
#include <unistd.h>

#include "wardog/daemon/daemon.hpp"
#include "wardog/daemon/logging.hpp"

int
main(int argc, char *argv[])
{
    wardog::LogLevel log_level = wardog::LogLevel::Debug;

    char *l = getenv("WARDOG_LOG_LEVEL");
    if (l && l[1] == '\0' && l[0] >= '0' && l[0] <= '4') {
        log_level = static_cast<wardog::LogLevel>(l[0] - '0');
    }

    // daemon requires specific group owner for socket
    // assume our gid if not specified
    gid_t tgt_gid = getgid();
    char *sgid = getenv("WARDOG_GID");
    if (sgid) {
        errno = 0;
        long lgid = strtol(sgid, nullptr, 10);

        // gid_t is typically an unsigned int
        if (errno == 0 && lgid >= 0 && lgid <= UINT_MAX)
            tgt_gid = lgid;
    }

    auto logger = wardog::Logger(log_level);

    try {
        if (argc > 2) {
            std::cout << "Usage: wardogd <wardog socket>" << std::endl;
            return 1;
        } else if (argc == 2) {
            logger.info("SOCKET ", argv[1]);
            auto daemon = wardog::WardogDaemon(argv[1], logger, tgt_gid);
            return daemon.run();
        } else if (char *p = getenv("WARDOG_SOCKET")) {
            logger.info("SOCKET ", p);
            auto daemon = wardog::WardogDaemon(p, logger, tgt_gid);
            return daemon.run();
        } else {
            logger.error("Could not find Wardog socket, try setting "
                         "WARDOG_SOCKET or passing as an argument");
            return 1;
        }
    } catch (const std::exception &e) {
        logger.error("Exception: ", e.what());
        return 1;
    } catch (...) {
        logger.error("Unknown exception");
        return 1;
    }
}
