#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int worker_count = 4;
    int executor = worker_count;  /* simulated executor */
    printf("Executor created with %d workers\n", executor);
    /* shutdown simulation */
    executor = 0;
    return rs;
}