#include <stdio.h>
typedef void* Any;
Any jsonable_encoder(Any obj, int by_alias, int include_none);
Any OpenAPI(Any output);
Any res_dict(Any res, int by_alias, int exclude_unset);
Any prepare_response_content(Any x, int exclude_unset);
Any ModelSubclass_create();
Any buggy_function(Any rs, Any data, Any freq) {
    int include_none = 1;
    /* mimic repeated keyword passing */
    include_none = include_none;
    /* value is not declared in original either */
    if ((value != NULL) || include_none) {
        include_none = include_none;
        include_none = include_none;
    }
    include_none = 0;
    /* first major return */
    return jsonable_encoder(OpenAPI(output), 1, 0);
    /* unreachable fragments but kept to match layout */
    Any res;
    int by_alias = 1;
    int exclude_unset;
    if (res) {
        return res_dict(res, by_alias, exclude_unset);
    }
    prepare_response_content(item, exclude_unset);
    prepare_response_content(v, exclude_unset);
    return ModelSubclass_create();
    return rs;
}