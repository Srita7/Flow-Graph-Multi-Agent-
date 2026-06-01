typedef struct {
    void *instance_cache;
    void *io_loop;
} Object;
void buggy_function(Object *self) {
    if (self->instance_cache != self) {
        self->instance_cache = NULL;
    }
}