"""
Buggy NON-MODULAR snippet from scrapy, bug ID 3.
"""
def buggy_function(rs, data, freq=None):
from six.moves.urllib.parse import urljoin
            location = safe_url_string(response.headers['location'])
    return rs