#include <cstring>
#include <unistd.h>

#include "wardog/daemon/client.hpp"
#include "wardog/daemon/types.hpp"

namespace wardog
{

static ssize_t
nbread(int fd, unsigned char *buf, size_t len)
{
    if (len == 0)
        return 0;

    size_t br = 0;
    while (br < len) {
        ssize_t res = read(fd, buf + br, len - br);
        if (res == -1) {
            if (errno == EINTR)
                continue;
            if (errno == EAGAIN || errno == EWOULDBLOCK)
                return br;
            return -1;
        } else if (res == 0)
            return br;

        br += res;
    }
    return br;
}

WardogClient::WardogClient(int fd, uint64_t id,
                           std::queue<WardogRequest> &rq_queue, Logger &logger)
    : m_fd(fd), m_id(id), m_rq_queue(rq_queue), m_logger(logger)
{
    m_logger.debug("CREATE ", m_id);
}

WardogClient::~WardogClient()
{
    m_logger.debug("DELETE ", m_id);
    close(m_fd);

    if (m_buf)
        delete[] m_buf;
}

ssize_t
WardogClient::handle_ev()
{
    ssize_t res;
    ssize_t total = 0;

    // read out as many requests as possible
    while (1) {
        if (m_buf == nullptr) {
            uint32_t sz_buf = 0;
            res = nbread(m_fd, reinterpret_cast<unsigned char *>(&sz_buf),
                         sizeof(sz_buf));

            if (res == -1) {
                subj_log_error("read", std::strerror(errno));
                return -1;
            }

            if (res == 0)
                return total;

            if (res != sizeof(sz_buf)) {
                subj_log_error("read", "incomplete length header");
                total += res;
                return total;
            }

            m_logger.trace(m_id, "(", m_fd, "): allocating buffer of ", sz_buf,
                           " bytes");

            m_buf_used = 0;
            m_buf_len = (size_t)sz_buf;
            m_buf = new unsigned char[m_buf_len];
        }

        unsigned char *st = m_buf + m_buf_used;
        res = nbread(m_fd, st, m_buf_len - m_buf_used);
        if (res == -1) {
            subj_log_error("read", std::strerror(errno));
            return -1;
        }

        if (res == 0)
            return total;

        m_logger.trace(m_id, "(", m_fd, "): read ", res, " bytes of request");

        m_buf_used += res;
        total += res;

        if (m_buf_used >= m_buf_len) {
            enum WardogErrorType error;
            std::vector<WardogRequest> msgs = WardogRequest::from_buffer(
                m_buf, m_buf_len, m_id, &error, m_logger);

            if (error != WARDOG_ERR_OK) {
                m_logger.error(m_id, "(", m_fd,
                               "): deserialise: failed with code ", error);
            } else {
                for (const auto &req : msgs)
                    m_rq_queue.push(req);
            }

            clear_buffer();
        }
    }

    return total;
}

void
WardogClient::clear_buffer()
{
    if (m_buf == nullptr)
        return;

    delete[] m_buf;
    m_buf = nullptr;
    m_buf_len = 0;
    m_buf_used = 0;
}

void
WardogClient::subj_log_error(const std::string &subj, const std::string &msg)
{
    m_logger.error(m_id, "(", m_fd, "): ", subj, ": ", msg);
}

}; // namespace wardog
