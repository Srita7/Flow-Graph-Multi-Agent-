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
        Any _model_subclass_result = ModelSubclass_create();
        return _model_subclass_result;
    }
    include_none = 0;
    Any _jsonable_result = jsonable_encoder(OpenAPI(output), 1, 0);
    /* unreachable fragments but kept to match layout */
    Any res;
    int by_alias = 1;
    int exclude_unset;
    res = prepare_response_content(_jsonable_result, exclude_unset);
    if (res) {
        return res_dict(res, by_alias, exclude_unset);
    }
    return rs