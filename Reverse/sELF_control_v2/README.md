# sELF control v2

### Category

Reverse

### Description

I've got this weird ELF, some stranger told me that I would be rewarded if I could fix it...

Can you help me ?


Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [EXECUTE_ME](EXECUTE_ME)

### Write up

To me the difficulty was to find the correct entry point. After that, it was pretty straightforward to see others bytes to patch: the goal was to have an `execve("/bin/sh")`.

The different patches were : 
- Entry point least significant byte: EP is at `0x08040020`
- `inc ebx`: increment the pointer in ebx to point to the "encrypted" /bin/sh
- `jmp 9`: instaead of "mov ah, 9", to jump to the /bin/sh decryption and syscall
- `rol DWORD [ebx], 0x11` istead of 11, to have a pointer to "/bin/sh" in EBX (first syscall parameter) and do an `execve("/bin/sh")` 

Final solve:
```
██╗  ██╗███████╗██████╗  ██████╗  ██████╗████████╗███████╗
██║  ██║██╔════╝██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝
███████║█████╗  ██████╔╝██║   ██║██║        ██║   █████╗  
██╔══██║██╔══╝  ██╔══██╗██║   ██║██║        ██║   ██╔══╝  
██║  ██║███████╗██║  ██║╚██████╔╝╚██████╗   ██║   ██║     
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝   ╚═╝   ╚═╝     
=============== sELF control v2 (by SoEasY) ===============


Offset of the byte to patch in hex (example: 18) : 18
Value to put at this offset in hex (example: 0C) : 20

Offset of the byte to patch in hex (example: 17) : 25
Value to put at this offset in hex (example: 1A) : 43

Offset of the byte to patch in hex (example: 02) : 3A
Value to put at this offset in hex (example: 05) : EB

Offset of the byte to patch in hex (example: 09) : 47
Value to put at this offset in hex (example: 04) : 11

[+] Execution : 
$ id
uid=1000(player) gid=1001(player) groups=1001(player),1000(ctf)
$ cat flag.txt
Hero{W0w_s0_y0u_4r3_4n_ELF_h34d3r_M4sT3r_but_d1d_y0u_kn0w_4b0ut_ELF_g0lfing???}
```

### Flag

```
Hero{W0w_s0_y0u_4r3_4n_ELF_h34d3r_M4sT3r_but_d1d_y0u_kn0w_4b0ut_ELF_g0lfing???}
```