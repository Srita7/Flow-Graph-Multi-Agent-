#include <stdio.h>
int buggy_function(int rs, char *data, int freq) {
    char *pool_id="pool1";
    int quantity=1;
    rs = printf("Pool: %s Quantity:%d\n",
            pool_id,
            quantity);
    return rs;
}