#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int is_list = 1;
    if(is_list)
    {
        printf("Convert list to tuple\n");
        printf("Serialize JSON\n");
    }
    return rs;
}