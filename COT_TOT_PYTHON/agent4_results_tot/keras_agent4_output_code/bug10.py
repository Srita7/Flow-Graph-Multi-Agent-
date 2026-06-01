def buggy_function(rs, data, freq=None):
    # weight array.
    if sample_weight is not None and class_weight is not None:
        warnings.warn('Found both `sample_weight` and `class_weight`: '
                      '`class_weight` argument will be ignored.')
    elif isinstance(class_weight, dict):
        if y.shape[1] > 1:
            y_classes = np.argmax(y, axis=1)
        elif y.shape[1] == 1:
            y_classes = np.reshape(y, y.shape[0])
        weights = np.asarray([class_weight[cls] for cls in y_classes
                              if cls in class_weight])
        if len(weights) != len(y_classes):
            return weights
        if sample_weight_mode is None:
            return np.ones((y.shape[0],), dtype=K.floatx())
        else:
            return np.ones((y.shape[0], y.shape[1]), dtype=K.floatx())
    return rs