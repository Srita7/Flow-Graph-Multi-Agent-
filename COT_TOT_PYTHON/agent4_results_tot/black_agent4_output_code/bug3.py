"""
Buggy NON-MODULAR snippet from black, bug ID 3.
"""
def buggy_function(rs, data, freq=None):
        rs = dict(exists=False, file_okay=True, dir_okay=False, readable=True, allow_dash=False)
    return rs