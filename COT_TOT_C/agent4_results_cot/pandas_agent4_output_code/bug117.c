#include <stdio.h>
typedef void* Any;
Any buggy_function(Any rs, Any data, Any freq) {
    if (is_series(data) || is_array(data) || is_index(data)) {
        /* missing body */
    }
    return rs;
}