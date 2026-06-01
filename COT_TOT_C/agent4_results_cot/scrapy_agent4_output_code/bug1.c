#include <stdio.h>
#include <string.h>
int buggy_function(int rs, char *data, int freq)
{
    char *allowed_domains[] = {"example.com","test.com",NULL};
    int i;
    char domain[]="example.com";
    for(i=0; allowed_domains[i]!=NULL; i++)
    {
        if(strcmp(domain,allowed_domains[i])==0)
        {
            printf("Domain matched\n");
        }
    }
    another_func();
    return rs;
}