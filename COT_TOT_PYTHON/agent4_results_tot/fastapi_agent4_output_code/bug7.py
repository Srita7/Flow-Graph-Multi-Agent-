"""
Buggy NON-MODULAR snippet from fastapi, bug ID 7.
"""
def buggy_function(rs, data, freq=None):
    error_response = {"status_code": HTTP_422_UNPROCESSABLE_ENTITY, "content": {"detail": exc.errors()}}
    return error_response