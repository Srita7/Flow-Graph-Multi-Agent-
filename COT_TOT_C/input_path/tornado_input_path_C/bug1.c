#include <assert.h>
typedef struct {
    int nodelay;
} Stream;
typedef struct {
    Stream *stream;
} Object;
void buggy_function(Object *self, int value) {
    assert(self->stream != NULL);
    self->stream->nodelay = value;
}