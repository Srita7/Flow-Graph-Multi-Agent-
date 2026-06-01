#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq)
{
    int is_fmt_on = 0;
    char *comments[] = {"FMT_ON", "FMT_OFF", "TEXT"};
    int i;
    for(i=0;i<3;i++)
    {
        if(strcmp(comments[i],"FMT_ON")==0)
            is_fmt_on = 1;
        else if(strcmp(comments[i],"FMT_OFF")==0)
            is_fmt_on = 0;
    }
    if(is_fmt_on)
        printf("Formatting ON\n");
    return rs;
}