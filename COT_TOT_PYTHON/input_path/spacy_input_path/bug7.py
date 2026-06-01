"""
Buggy NON-MODULAR snippet from spacy, bug ID 7.
"""
def buggy_function(rs, data, freq=None):
Last tested with: v2.1.0
        get_sort_key = lambda span: (span.end - span.start, span.start)
                seen_tokens.update(range(span.start, span.end))
        get_sort_key = lambda span: (span.end - span.start, span.start)
    return rs
