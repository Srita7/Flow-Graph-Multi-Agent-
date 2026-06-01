#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int columns = 3;
    if(columns > 0)
    {
        printf("Columns exist\n");
    }
    return columns;
}