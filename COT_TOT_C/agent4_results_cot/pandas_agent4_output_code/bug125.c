#include <stdio.h>
typedef void* Any;
Any buggy_function(Any rs, Any data, Any freq) {
    buggy_function(rs, data, freq);
    return rs;
}