"""
Buggy NON-MODULAR snippet from fastapi, bug ID 10.
(No code found for buggy version.)
"""
def buggy_function(rs, data, freq=None):
    if freq:
        rs = data.resample(freq).mean()
    return rs