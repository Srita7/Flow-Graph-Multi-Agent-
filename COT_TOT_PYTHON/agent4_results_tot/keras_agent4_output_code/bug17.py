"""
Buggy NON-MODULAR snippet from keras, bug ID 17.
"""
def buggy_function(rs, data, freq=None):
    return K.cast(K.equal(K.max(y_true, axis=-1),
    return rs