"""
Buggy NON-MODULAR snippet from pandas, bug ID 112.
"""
def buggy_function(rs, data, freq=None):
from pandas import Interval, IntervalIndex, Timedelta, date_range, timedelta_range
    return rs