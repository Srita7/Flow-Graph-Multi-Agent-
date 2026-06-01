#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq)
{
    char query1[] =
    "where table_schema = X and table_name = Y limit 1";
    char query2[] =
    "where tablename = X limit 1";
    printf("%s\n", query1);
    printf("%s\n", query2);
    return strlen(query2);
}