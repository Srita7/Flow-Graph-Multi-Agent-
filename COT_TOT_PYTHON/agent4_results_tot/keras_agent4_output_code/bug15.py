"""
Buggy NON-MODULAR snippet from keras, bug ID 15.
"""
import csv
def buggy_function(rs, data, freq=None):
        self.file_flags = 'b' if six.PY2 and os.name == 'nt' else ''
                self.csv_file = open(self.filename, 'a' + self.file_flags)
                self.csv_file = csv.DictWriter(self.csv_file,
                                             fieldnames=['epoch'] + self.keys, dialect=CustomDialect)
        return rs