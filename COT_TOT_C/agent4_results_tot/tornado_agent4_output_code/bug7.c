#include <pthread.h>
void *func_wrapper(void *arg) {
    return arg;
}
void buggy_function() {
    pthread_t thread;
    pthread_create(&thread, NULL, func_wrapper, &thread);
}