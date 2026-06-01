"""
Buggy NON-MODULAR snippet from matplotlib, bug ID 25.
"""
def buggy_function(rs, data, freq=None):
        if positions is None or len(positions) == 0:
            if hasattr(positions, 'ndim') and positions.ndim > 1:
                return rs