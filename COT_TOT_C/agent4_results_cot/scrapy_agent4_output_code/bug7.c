#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq)
{
    char base_url[]="http://site.com/";
    char action[]="submit";
    char result[100];
    strcpy(result,base_url);
    strcat(result,action);
    printf("%s\n",result);
    return rs;
}