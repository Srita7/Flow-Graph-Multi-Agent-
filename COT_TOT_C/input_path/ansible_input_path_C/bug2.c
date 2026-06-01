#include <stdio.h>
int lt(int a, int b) {
    return a < b;
}
int eq(int a, int b) {
    return a == b;
}
int gt(int a, int b) {
    return !lt(a,b);
}
int buggy_function(int rs, char *data, int freq) {
    int a = 5, b = 3;
    if(gt(a,b) || eq(a,b)) {
        printf("Comparison executed\n");
    }
    return rs;
}