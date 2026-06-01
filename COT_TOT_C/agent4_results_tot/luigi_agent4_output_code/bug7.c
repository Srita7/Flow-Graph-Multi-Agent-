#include <stdio.h>
#define RUNNING 1
#define BATCH_RUNNING 2
#define PENDING 3
int buggy_function(int rs, char *data, int freq)
{
    int task_status = RUNNING;
    int status = PENDING;
    int new_deps = 0;
    if(!((task_status==RUNNING || task_status==BATCH_RUNNING)
        && status==PENDING) || new_deps)
    {
        printf("Reschedule allowed\n");
    }
    return rs;
}