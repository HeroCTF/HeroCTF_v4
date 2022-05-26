#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    const char *procs[3];
    genprocs(procs);

    int nb_procs = sizeof(procs)/sizeof(procs[0]);
    for (int i = 0 ; i < nb_procs ; i++) {
        
        char *arg1 = procs[i];
        
        printf("\t[*] Killing server %s\n", procs[i]);
        
        int pid = fork();
        if(pid == 0) {
            execl("/usr/bin/pkill", "/usr/bin/pkill", arg1, NULL);
        }
        else if (pid > 0) {
            int status;
            waitpid(pid, &status, 0);
        }
        else {
            printf("[!] Error while forking");
        }
    }

    return 1;
}