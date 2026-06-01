"""
Buggy NON-MODULAR snippet from pandas, bug ID 111.
"""
def buggy_function(rs, data, freq=None):
                    return self._invalid_indexer("label", key)
                        return self._invalid_indexer("label", key)
            if self.categories._defer_to_indexing:
                rs = self.categories._convert_scalar_indexer(key, kind=kind)
    return rs