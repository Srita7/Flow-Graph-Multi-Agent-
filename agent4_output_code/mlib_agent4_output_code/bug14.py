"""
Buggy NON-MODULAR snippet from matplotlib, bug ID 14.
"""
def buggy_function(rs, data, freq=None):
        # Update bbox last, as it depends on font properties.
    return rs