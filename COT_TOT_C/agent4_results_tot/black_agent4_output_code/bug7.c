#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int index = 1;
    printf("Insert child at %d\n", index);
    return index;
}