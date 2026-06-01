#include <stdio.h>
int clone_parent()
{
    printf("Clone parent\n");
    return 0;
}
int requires()
{
    clone_parent();
    buggy_function();
    return 0;
}
int buggy_function(int rs, char *data, int freq)
{
    clone_parent();
    return rs;
}