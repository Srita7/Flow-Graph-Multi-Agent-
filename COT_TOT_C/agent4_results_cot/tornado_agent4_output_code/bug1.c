#include <assert.h>
typedef struct Stream {
    int nodelay;
} Stream;
typedef struct {
    Stream *stream;
} Object;
void buggy_function(Object *self, int value) {
    assert(self->stream != NULL);
    self->stream->nodelay = value;
}