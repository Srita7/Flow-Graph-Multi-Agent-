#include <stdio.h>
int clone_parent()
{
    printf("Clone parent\n");
    return 0;
}
int requires()
{
    clone_parent();
    return 0;
}
int buggy_function(int rs, char *data, int freq)
{
    clone_parent();
    requires();
    return rs;
}