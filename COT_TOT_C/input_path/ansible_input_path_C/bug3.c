#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq) {
    char path[] = "/etc/lsb-release";
    if(strcmp(path,"/etc/lsb-release")==0 &&
       strstr(data,"Kali")!=NULL)
    {
        printf("Matched\n");
    }
    return rs;
}