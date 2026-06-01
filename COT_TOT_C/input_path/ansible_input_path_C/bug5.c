#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq) {
    char msg[100] = "missing required arguments";
    char expected[] =
    "TypeError(parameters are mutually exclusive)";
    printf("%s\n",msg);
    printf("%s\n",expected);
    return rs;
}