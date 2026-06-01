#include <stdio.h>
typedef void* Any;
Any buggy_function(Any rs, Any data, Any freq) {
    return NULL;   /* mirrors empty return () */
    return rs;
}