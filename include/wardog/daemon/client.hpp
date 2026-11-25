#ifndef client_hpp_INCLUDED
#define client_hpp_INCLUDED

#include <cstdint>
#include <queue>

#include "wardog/daemon/logging.hpp"
#include "wardog/daemon/types.hpp"

namespace wardog
{

class WardogClient
{
private:
    int m_fd = -1;
    uint64_t m_id = 0;

    unsigned char *m_buf = nullptr;
    size_t m_buf_len = 0;
    size_t m_buf_used = 0;

    std::queue<WardogRequest> &m_rq_queue;
    Logger &m_logger;

    void clear_buffer();
    void subj_log_error(const std::string &subj, const std::string &msg);

public:
    WardogClient(int fd, uint64_t id, std::queue<WardogRequest> &rq_queue,
                 Logger &logger);
    ~WardogClient();

    ssize_t handle_ev();

    int
    fd()
    {
        return m_fd;
    }

    uint64_t
    id()
    {
        return m_id;
    }
};

}; // namespace wardog

#endif // client_hpp_INCLUDED
