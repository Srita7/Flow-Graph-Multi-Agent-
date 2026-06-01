"""
Buggy NON-MODULAR snippet from tornado, bug ID 6.
"""
def buggy_function(rs, data, freq=None):
    import weakref
    _ioloop_for_asyncio = weakref.WeakKeyDictionary()
    return rs