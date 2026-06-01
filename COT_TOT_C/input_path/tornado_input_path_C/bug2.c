#include <string.h>
int buggy_function(char *headers) {
    if (strstr(headers, "Transfer-Encoding") == NULL) {
        return 1;
    }
    return 0;
}