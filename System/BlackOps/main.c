#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void)
{
    puts("[*] Cleaning all servers");

    setreuid(geteuid(), geteuid());

    // Make sure shared libraries are linked
    system("/sbin/ldconfig");

    int pid1 = fork();
    if(pid1 == 0) {
        execl("/bin/kc", "/bin/kc", NULL);
    }
    else if (pid1 > 0) {
        int status;
        waitpid(pid1, &status, 0);
    }
    else {
        printf("[!] Error while forking");
    }
    puts("[*] All servers cleaned");

    puts("[*] Restart services");

    // Javasript server
    int pid2 = fork();
    if(pid2 == 0) {
        execl("/home/user1/servers/src/server.js", "/home/user1/servers/src/server.js", NULL);
    }
    else if (pid2 == -1) {
        printf("[!] Error while forking");
    }

    // Go server
    int pid3 = fork();
    if(pid3 == 0) {
        execl("/home/user1/servers/src/server.go", "/home/user1/servers/src/server.go", NULL);
    }
    else if (pid3 == -1) {
        printf("[!] Error while forking");
    }

    // Python server
    int pid4 = fork();
    if(pid4 == 0) {
        execl("/home/user1/servers/src/server.py", "/home/user1/servers/src/server.py", NULL);
    }
    else if (pid4 == -1) {
        printf("[!] Error while forking");
    }



    puts("[*] Services restarted");
}