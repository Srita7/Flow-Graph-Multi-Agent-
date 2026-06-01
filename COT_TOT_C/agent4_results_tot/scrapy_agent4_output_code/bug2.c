#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int size = 5;
    int limit = 3;
    while(size >= limit)
    {
        size--;
        printf("Pop item: %d\n", size);
    }
    return size;
}