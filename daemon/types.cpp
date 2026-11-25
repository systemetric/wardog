#include "wardog/daemon/types.hpp"
#include "wardog/daemon/logging.hpp"
#include <cstring>
#include <memory>

namespace wardog
{

static const struct WardogArgument EMPTY_ARGUMENT{};
static const struct WardogRequest EMPTY_REQUEST{};

static size_t
strlen_max(unsigned char *buf, size_t max, unsigned char **endptr)
{
    if (max == 0)
        return 0;

    size_t count = 0;
    while (*buf && count < max) {
        buf++;
        count++;
    }

    if (endptr)
        *endptr = buf;
    return count;
}

std::vector<WardogRequest>
WardogRequest::from_buffer(unsigned char *buf, size_t len, uint64_t client_id,
                           enum WardogErrorType *error, Logger &logger)
{
    logger.trace("deserialising request buffer, ", len, " bytes:");

    // too short for any valid messages?
    if (len < 3) {
        logger.trace("  payload length too short");
        *error = WARDOG_ERR_INVALID;
        return std::vector<WardogRequest>();
    }

    *error = WARDOG_ERR_OK;

    uint8_t nmsgs = static_cast<uint8_t>(buf[0]);
    std::vector<WardogRequest> msgs;
    WardogRequest req = EMPTY_REQUEST;

    size_t left = len - 1;
    unsigned char *st = &buf[1];

    for (int i = 0; i < nmsgs && left > 0; i++) {
        if (left < 2) {
            logger.trace("   payload length too short");
            *error = WARDOG_ERR_INVALID;
            return std::vector<WardogRequest>();
        }

        req.client_id = client_id;

        uint8_t mode = st[0];
        switch (mode) {
            case WARDOG_RQ_GET:
                req.mode = WARDOG_RQ_GET;
                break;
            case WARDOG_RQ_SET:
                req.mode = WARDOG_RQ_SET;
                break;
            case WARDOG_RQ_PROBE:
                req.mode = WARDOG_RQ_PROBE;
                break;
            default:
                logger.trace("  invalid message request mode ", mode);
                *error = WARDOG_ERR_INVALID;
                return std::vector<WardogRequest>();
        }

        uint8_t nargs = st[1];

        left -= 2;
        st += 2;

        WardogArgument arg = EMPTY_ARGUMENT;
        for (int j = 0; j < nargs && left > 0; j++) {
            uint8_t type = st[0];
            left -= 1;
            st += 1;

            size_t arg_len = 0;
            switch (type) {
                case WARDOG_TYPE_BYTE:
                    arg.type = WARDOG_TYPE_BYTE;
                    arg_len = sizeof(uint8_t);
                    break;
                case WARDOG_TYPE_WORD:
                    arg.type = WARDOG_TYPE_WORD;
                    arg_len = sizeof(uint16_t);
                    break;
                case WARDOG_TYPE_DWORD:
                    arg.type = WARDOG_TYPE_DWORD;
                    arg_len = sizeof(uint32_t);
                    break;
                case WARDOG_TYPE_DOUBLE:
                    arg.type = WARDOG_TYPE_DOUBLE;
                    arg_len = sizeof(double);
                    break;
                case WARDOG_TYPE_STRING: {
                    unsigned char *endptr = nullptr;
                    arg.type = WARDOG_TYPE_STRING;
                    arg_len = strlen_max(&st[0], left, &endptr) + 1;

                    if (!endptr || *endptr) {
                        logger.trace("  unterminated string");
                        *error = WARDOG_ERR_INVALID;
                        return std::vector<WardogRequest>();
                    }

                    break;
                }
                default:
                    logger.trace("  invalid argument type ", type);
                    *error = WARDOG_ERR_INVALID;
                    return std::vector<WardogRequest>();
            }

            if (left < arg_len) {
                logger.trace("  payload length too short");
                *error = WARDOG_ERR_INVALID;
                return std::vector<WardogRequest>();
            }

            arg.data = std::make_shared<unsigned char[]>(arg_len);
            std::memcpy(arg.data.get(), reinterpret_cast<void *>(&st[0]),
                        arg_len);

            left -= arg_len;
            st += arg_len;

            req.args.push_back(arg);
            arg = EMPTY_ARGUMENT;
        }

        msgs.push_back(req);
        req = EMPTY_REQUEST;
    }

    if (msgs.size() < nmsgs) {
        logger.trace("  payload length too short");
        *error = WARDOG_ERR_INVALID;
        return std::vector<WardogRequest>();
    }

    if (left > 0) {
        logger.trace("  trailing bytes after messages");
        *error = WARDOG_ERR_INVALID;
        return std::vector<WardogRequest>();
    }

    logger.trace("  deserialised ", msgs.size(), " messages");
    return msgs;
}

}; // namespace wardog
