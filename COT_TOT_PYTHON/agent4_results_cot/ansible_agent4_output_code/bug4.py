"""
Buggy NON-MODULAR snippet from ansible, bug ID 4.
"""
def buggy_function(rs, data, freq=None):
    _collections = FieldAttribute(isa='list', listof=string_types, priority=100, default=_ensure_default_collection)
    return rs