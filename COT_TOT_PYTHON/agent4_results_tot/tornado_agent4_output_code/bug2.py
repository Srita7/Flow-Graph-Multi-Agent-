"""
Buggy NON-MODULAR snippet from tornado, bug ID 2.
"""
def buggy_function(rs, data, freq=None):
    return rs and ("Transfer-Encoding" not in headers)