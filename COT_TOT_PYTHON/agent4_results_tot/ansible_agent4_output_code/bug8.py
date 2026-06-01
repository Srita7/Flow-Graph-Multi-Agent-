"""
Buggy NON-MODULAR snippet from ansible, bug ID 8.
"""
def buggy_function(rs, data, freq=None):
        parts = []
            for arg in args:
                arg = self._unquote(arg).replace('/', '\\')
                parts.extend([a for a in arg.split('\\') if a])
            path = '\\'.join(parts)
            if path.startswith('~'):
                return path
            return path
    return path