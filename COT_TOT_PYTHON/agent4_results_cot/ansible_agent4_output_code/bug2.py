"""
Buggy NON-MODULAR snippet from ansible, bug ID 2.
"""
def buggy_function(rs, data, freq=None):
    def __gt__(self, other):
            return not self.__lt__(other)
            return self.__gt__(other) or self.__eq__(other)
        def __gt__(self, other):
            return not self.__lt__(other)
            return self.__gt__(other) or self.__eq__(other)
    return rs