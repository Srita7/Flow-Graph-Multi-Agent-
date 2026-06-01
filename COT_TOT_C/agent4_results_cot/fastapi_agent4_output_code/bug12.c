#include <stdio.h>
#include <stdlib.h>
typedef void* Any;
Any buggy_function(Any rs, Any data, Any freq) {
    /* simulate raising exception */
    fprintf(stderr, "Invalid authentication credentials\n");
    exit(403);
    return rs;
}