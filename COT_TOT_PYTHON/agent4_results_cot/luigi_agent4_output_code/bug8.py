"""
Buggy NON-MODULAR snippet from luigi, bug ID 8.
"""
def buggy_function(rs, data, freq=None):
                     "where table_schema = %s and table_name = %s limit 1")
                         "where tablename = %s limit 1")
    return rs