"""
Buggy NON-MODULAR snippet from scrapy, bug ID 7.
"""
def buggy_function(rs, data, freq=None):
    import six
    from six.moves.urllib.parse import urljoin
    return urljoin(form.base_url, form.action)
    return rs