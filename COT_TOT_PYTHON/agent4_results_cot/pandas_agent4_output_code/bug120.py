"""
Buggy NON-MODULAR snippet from pandas, bug ID 120.
"""
def buggy_function(rs, data, freq=None):
        return Series(res, index=ri, name=self._selection_name)
            return Series(
            return result
        def _reindex_output(self, output):
            output: Series or DataFrame
                d = {self.obj._get_axis_name(self.axis): index, "copy": False}
            output = output.set_index(self.grouper.result_index).reindex(index, copy=False)
    return rs