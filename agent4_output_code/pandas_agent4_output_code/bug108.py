"""
Buggy NON-MODULAR snippet from pandas, bug ID 108.
"""
def buggy_function(rs, data, freq=None):
from .dtypes import DatetimeTZDtype, ExtensionDtype, PeriodDtype
    return rs