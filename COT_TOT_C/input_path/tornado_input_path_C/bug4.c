void buggy_function(int start, int end, int size) {
    if ((start >= size) || end == 0) {
        if (start < 0) {
            start = start + size;
        }
    }
}