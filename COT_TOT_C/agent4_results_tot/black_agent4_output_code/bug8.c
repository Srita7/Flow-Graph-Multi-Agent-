#include <stdio.h>
int buggy_function(int rs, char *data, int freq)
{
    char leaves[10] = "abc";
    int last_is_comma = 0;
    if(!last_is_comma && leaves[0] != '\0')
    {
        int print_result = printf("Add comma\n");
        rs = print_result;
    }
    return rs;
}