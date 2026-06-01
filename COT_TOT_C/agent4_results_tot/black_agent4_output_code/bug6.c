#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int target_version = 35;
    if(target_version == 27)
        printf("Python 2.7\n");
    else if(target_version == 33)
        printf("Python 3.3\n");
    else if(target_version == 34)
        printf("Python 3.4\n");
    else if(target_version == 35)
        printf("Python 3.5\n");
    /* token generation simulation */
    printf("Generating tokens\n");
    return rs;
}