#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int exists = 0;
    int file_okay = 1;
    int dir_okay = 0;
    int readable = 1;
    int allow_dash = 0;
    printf("File flags set\n");
    return rs;
}