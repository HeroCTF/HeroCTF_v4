#include <stdlib.h>
#include <stdio.h>

int main() {
    printf("Not sure why, but I'm gonna set my ruid to my uid.\n");
    setreuid(geteuid(), geteuid());
    printf("Not sure why, but I'm gonna run the 'WTFFFFF' program right now.\n");
    system("./WTFFFFF");
    return 0;
}