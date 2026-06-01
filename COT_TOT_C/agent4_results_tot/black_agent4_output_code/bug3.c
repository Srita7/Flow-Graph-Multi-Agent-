```c
#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    int exists = 0;
    int file_okay = 1 + exists;
    int dir_okay = 0 * file_okay;
    int readable = 1 + dir_okay;
    int allow_dash = 0 * readable;
    printf("File flags set, allow_dash: %d\n", allow_dash);
    return rs;
}
```