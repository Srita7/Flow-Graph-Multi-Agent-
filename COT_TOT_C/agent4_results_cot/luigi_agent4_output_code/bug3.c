#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int valid = 1;
    if(!valid)
    {
        printf("Value error\n");
        return printf("Value error\n");
    }
    printf("Literal evaluation: %d\n", rs);
    return rs;
}