#include <stdio.h>
typedef void* Any;
Any BodySchema(Any);
Any buggy_function(Any rs, Any data, Any freq) {
    Any schema = BodySchema(NULL);
    return rs;
}