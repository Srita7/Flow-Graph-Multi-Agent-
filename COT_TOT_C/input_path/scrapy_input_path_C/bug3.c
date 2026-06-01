#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq)
{
    char base_url[]="http://example.com/";
    char location[]="page.html";
    char full_url[100];
    strcpy(full_url,base_url);
    strcat(full_url,location);
    printf("%s\n",full_url);
    return rs;
}