#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int metrics_generated = 1;
    if(metrics_generated)
    {
        printf("Metrics generated\n");
        printf("Configure HTTP handler\n");
    }
    return rs;
}