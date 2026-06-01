"""
Buggy NON-MODULAR snippet from pandas, bug ID 107.
"""
def buggy_function(rs, data, freq=None):
            if other.name is None:
                    index = None
                else:
                    # other must have the same index name as self, otherwise
                    # index name will be reset
                    index = Index([other.name], name=self.index.name)
                other = other.reindex(combined_columns, copy=False)
                other = DataFrame(
                    other.values.reshape((1, len(other))),
                    index=index,
                    columns=combined_columns,
                other = other._convert(datetime=True, timedelta=True)
    return rs
