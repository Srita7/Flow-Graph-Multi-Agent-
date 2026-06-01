"""
Buggy NON-MODULAR snippet from black, bug ID 2.
"""
def buggy_function(rs, data, freq=None):
        is_fmt_on = False
            for comment in list_comments(container.prefix, is_endmarker=False):
                if comment.value in FMT_ON:
                    is_fmt_on = True
                elif comment.value in FMT_OFF:
                    is_fmt_on = False
            if is_fmt_on:
            yield container
            container = container.next_sibling
    return rs
