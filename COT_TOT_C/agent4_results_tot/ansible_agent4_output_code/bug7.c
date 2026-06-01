#include <stdio.h>
int buggy_function(int rs, char *data, int freq) {
    char *to_remove[]={"a","b","c"};
    int i;
    for(i=0;i<3;i++)
    {
        printf("no %s\n",to_remove[i]);
    }
    return rs;
}