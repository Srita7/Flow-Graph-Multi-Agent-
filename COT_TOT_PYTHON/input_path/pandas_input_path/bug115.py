"""
Buggy NON-MODULAR snippet from pandas, bug ID 115.
"""
def buggy_function(rs, data, freq=None):
        result[invalid] = np.interp(inds[invalid], inds[valid], yvalues[valid])
    return rs
