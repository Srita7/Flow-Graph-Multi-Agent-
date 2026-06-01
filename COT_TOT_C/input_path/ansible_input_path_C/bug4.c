#include <stdio.h>
int buggy_function(int rs, char *data, int freq) {
    char *collections = "list";
    printf("Collection type: %s\n",collections);
    return rs;
}