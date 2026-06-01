#include <stdio.h>
typedef void* Any;
Any buggy_function(Any rs, Any data, Any freq) {
    Any csv_file;
    Any self_file_flags;

    self_file_flags = (six_py2 && is_windows()) ? 'b' : 0;
    csv_file = open_file(filename, "a");
    csv_file = open_file(filename, "w");
    return create_csv_writer(csv_file);
}