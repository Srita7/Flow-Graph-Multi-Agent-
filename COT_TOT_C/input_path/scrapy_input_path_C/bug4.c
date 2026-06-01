#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    char failure_value[]="Error";
    char failure_type[]="Type";
    char traceback[]="Trace";
    printf("%s %s %s\n",
           failure_value,
           failure_type,
           traceback);
    return rs;
}