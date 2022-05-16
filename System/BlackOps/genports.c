#include <stdio.h>
 
 
void genports(int *buf)
{
    int start = 9090;
    for (int i = start; i < start+3; i++)
    {
        buf[i-start] = i; 
    }
}