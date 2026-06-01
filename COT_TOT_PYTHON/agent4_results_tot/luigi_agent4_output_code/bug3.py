"""
Buggy NON-MODULAR snippet from luigi, bug ID 3.
"""
def buggy_function(rs, data, freq=None):
    try:
        pass
    except ValueError:
        return literal_eval(x)  # if this causes an error, let that error be raised.
    return rs