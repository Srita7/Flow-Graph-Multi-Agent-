"""
Buggy NON-MODULAR snippet from luigi, bug ID 6.
"""
def buggy_function(rs, data, freq=None):
    if isinstance(data, list):
        class _DictParamEncoder(JSONEncoder):
            """
            JSON encoder for :py:class:`~DictParameter`, which makes :py:class:`~_FrozenOrderedDict` JSON serializable.
            """
            def default(self, obj):
                if isinstance(obj, _FrozenOrderedDict):
                    return obj.get_wrapped()
                return json.JSONEncoder.default(self, obj)
            return json.dumps(x, cls=DictParameter._DictParamEncoder)
            Ensure that list parameter is converted to a tuple so it can be hashed.
            return list(json.loads(x))
            return json.dumps(x)
    class TupleParameter(Parameter):
                return tuple(tuple(x) for x in json.loads(x))  # loop required to parse tuple of tuples
        def serialize(self, x):
            """
            Opposite of :py:meth:`parse`.
            Converts the value ``x`` to a string.
            :param x: the value to serialize.
            """
            return json.dumps(x)
    return rs