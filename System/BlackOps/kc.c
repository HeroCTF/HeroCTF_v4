#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    int ports[3];
    genports(ports);

    int nb_ports = sizeof(ports)/sizeof(ports[0]);
    for (int i = 0 ; i < nb_ports ; i++) {
        
        char *arg1 = (char*)malloc(5 * sizeof(char));
        sprintf(arg1, "%d/tcp", ports[i]);

        char *arg2 = "-k";
        
        printf("\t[*] Killing port %d\n", ports[i]);
        
        int pid = fork();
        if(pid == 0) {
            execl("/bin/fuser", "/bin/fuser", arg1, arg2, NULL);
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