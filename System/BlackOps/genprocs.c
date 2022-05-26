#include <stdio.h>
 
 
void genprocs(char *buf[])
{
    char *procs[3] = {"server.js", "server.go", "server.py"};

    for (int i = 0 ; i < 3 ; i++) {
        buf[i] = procs[i];
    }
}