#ifndef types_hpp_INCLUDED
#define types_hpp_INCLUDED

#include <cstdint>
#include <memory>
#include <vector>

#include "wardog/daemon/logging.hpp"

namespace wardog
{

/*
    Wardog payload format:
        < length > < nmsgs > [ message ] ...
        - length: uint32_t, length of rest of payload
        - nmsgs: uint8_t, number of messages

    Wardog message format:
        < context > < nargs > [ arg ] ...
        - context: uint8_t, request mode; error bits; etc.
        - nargs: uint8_t, number of arguments in this message

    Wardog argument format:
        < type > < value >
        - type: uint8_t, the type of this argument
        - value: the actual argument itself

    all values are little-endian *always*
*/

enum WardogRequestMode {
    WARDOG_RQ_GET = 1,   // get a property of a node
    WARDOG_RQ_SET = 2,   // set a property of a node
    WARDOG_RQ_PROBE = 3, // probe a node
};

enum WardogType {
    WARDOG_TYPE_BYTE = 1,   // uint8_t
    WARDOG_TYPE_WORD = 2,   // uint16_t
    WARDOG_TYPE_DWORD = 3,  // uint32_t
    WARDOG_TYPE_DOUBLE = 4, // double
    WARDOG_TYPE_STRING = 5, // null-terminated utf-8 string
};

enum WardogErrorType {
    WARDOG_ERR_OK = 0,
    WARDOG_ERR_INVALID = 1,
};

struct WardogArgument {
    enum WardogType type;
    std::shared_ptr<unsigned char[]> data;
};

struct WardogRequest {
    enum WardogRequestMode mode;
    std::vector<WardogArgument> args;
    uint64_t client_id;

    static std::vector<WardogRequest>
    from_buffer(unsigned char *buf, size_t len, uint64_t client_id,
                enum WardogErrorType *error, Logger &logger);
};

}; // namespace wardog

#endif // types_hpp_INCLUDED
