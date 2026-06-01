#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int before = 10;
    int previous_after = 5;
    before -= previous_after;
    printf("%d\n", before);
    return rs;
}