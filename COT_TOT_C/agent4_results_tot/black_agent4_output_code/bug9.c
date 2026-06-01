#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int python2 = 1;
    if(python2)
    {
        printf("Use Python2 grammar\n");
    }
    return rs;
}