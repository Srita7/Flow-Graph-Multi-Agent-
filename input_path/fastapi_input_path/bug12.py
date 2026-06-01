"""
Buggy NON-MODULAR snippet from fastapi, bug ID 12.
"""
def buggy_function(rs, data, freq=None):
            raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
    return rs
