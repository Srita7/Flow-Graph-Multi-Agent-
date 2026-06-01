"""
Buggy NON-MODULAR snippet from spacy, bug ID 3.
"""
def buggy_function(rs, data, freq=None):
text_regex = re.compile(r"(?<=<text xml:space=\"preserve\">).*(?=</text)")
        text_search = text_regex.search(article_text)
    return text_search