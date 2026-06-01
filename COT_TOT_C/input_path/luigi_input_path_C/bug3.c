#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int valid = 1;
    if(!valid)
    {
        printf("Value error\n");
        return rs;
    }
    printf("Literal evaluation\n");
    return rs;
}