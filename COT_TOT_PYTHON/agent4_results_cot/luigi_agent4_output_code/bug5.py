"""
Buggy NON-MODULAR snippet from luigi, bug ID 5.
"""
def buggy_function(rs, data, freq=None):
        # Modify task_that_inherits by subclassing it and adding methods
            @task._task_wraps(task_that_inherits)
            class Wrapped(task_that_inherits):
                def clone_parent(_self, **args):
                    return _self.clone(cls=self.task_to_inherit, **args)
            return Wrapped
            # Modify task_that_requres by subclassing it and adding methods
            @task._task_wraps(task_that_requires)
            class Wrapped(task_that_requires):
                def requires(_self):
                    return _self.clone_parent()
            return Wrapped
    return rs