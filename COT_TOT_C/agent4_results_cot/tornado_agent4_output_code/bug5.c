typedef struct {
    double callback_time;
} Object;
double buggy_function(Object *self) {
    double callback_time_sec;
    callback_time_sec = self->callback_time / 1000.0;
    return callback_time_sec;
}