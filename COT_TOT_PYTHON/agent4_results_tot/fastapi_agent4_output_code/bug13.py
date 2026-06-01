```python
"""
Buggy NON-MODULAR snippet from fastapi, bug ID 13.
"""
def buggy_function(rs, data, freq=None):
                if responses is None:
                        responses = {}
                responses = {**responses, **route.responses}
                        responses=responses,
                        return rs, (responses=responses,)
```