"""
Buggy NON-MODULAR snippet from keras, bug ID 15.
"""
def buggy_function(rs, data, freq=None):
        self.file_flags = 'b' if six.PY2 and os.name == 'nt' else ''
                self.csv_file = open(self.filename, 'a' + self.file_flags)
                self.csv_file = open(self.filename, 'w' + self.file_flags)
                                             fieldnames=['epoch'] + self.keys, dialect=CustomDialect)
    return rs
