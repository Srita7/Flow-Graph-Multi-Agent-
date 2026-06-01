#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq) {
    char version[]="*";
    char requirement[]="*";
    int parent=1;
    if(parent && strcmp(version,"*")==0 &&
       strcmp(requirement,"*")!=0)
    {
        return rs;
    }
    else if(strcmp(requirement,"*")==0 ||
            strcmp(version,"*")==0)
    {
        printf("Continue\n");
    }
    return rs;
}