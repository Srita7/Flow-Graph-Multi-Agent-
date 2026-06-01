#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq) {
    char path[100]="test\\folder";
    if(path[0]=='~')
        return strlen(path);
    printf("%s\n",path);
    return strlen(path);
}