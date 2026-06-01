"""
Buggy NON-MODULAR snippet from pandas, bug ID 100.
"""
def buggy_function(rs, data, freq=None):
    rs = rs.loc[~rs.index.duplicated()]
    rs = rs.reindex_like(data)
    if freq is None:
        mask = isna(com.values_from_object(data))
        np.putmask(rs.values, mask, np.nan)
    return rs