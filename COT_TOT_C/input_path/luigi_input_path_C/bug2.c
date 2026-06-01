#include <stdio.h>
#include <stdlib.h>
int buggy_function(int rs, char *data, int freq)
{
    char project[] = "proj";
    char dataset[] = "data";
    char table[] = "table";
    printf("%s:%s.%s\n", project, dataset, table);
    int supported = 1;
    if(!supported)
    {
        printf("Target not supported\n");
        exit(1);
    }
    return rs;
}