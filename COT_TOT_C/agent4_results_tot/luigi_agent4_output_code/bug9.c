#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int failed = 1;
    int pending = 0;
    int completed = 0;
    int scheduling_error = 0;
    if(failed)
    {
        char smiley[] = ":(";
        char reason[] = "failed tasks";
        printf("%s %s\n", smiley, reason);
        if(scheduling_error)
        {
            printf("Scheduling error\n");
        }
    }
    return rs;
}