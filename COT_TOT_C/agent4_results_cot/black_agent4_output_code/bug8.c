#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    char leaves[10] = "abc";
    int last_is_comma = 0;
    if(!last_is_comma)
    {
        printf("Add comma\n");
    }
    return rs;
}