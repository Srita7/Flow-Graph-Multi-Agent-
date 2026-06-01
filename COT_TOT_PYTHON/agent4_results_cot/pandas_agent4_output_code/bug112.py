def buggy_function(rs, data, freq=None):
    """
    Buggy NON-MODULAR snippet from pandas, bug ID 112.
    """
    from pandas import Interval, IntervalIndex, Timedelta, date_range, timedelta_range
    return rs