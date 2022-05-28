# MVBN

### Category

Reverse

### Description

Some french student told me about a «Machine Virtuelle de Bas Niveau» project, but I don't speak french.

Do you know what he was talking about ?

Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [MVBN.s](MVBN.s)

### Write up

Here we've got an LLVM IR (Intermediate Representation) file. The easiest way to reverse is probably to compile it to make an ELF and reverse it afterwards.
- compile LLVM IR to ELF x64 (without linking) : `llc -o MVBN.o MVBN.s -filetype=obj`
- link libc : `gcc -no-pie -o MVBN MVBN.o`

Then we can launch our `MVBN` binary:
```bash
$ ./MVBN 
Usage: ./MVBN <flag>
$ ./MVBN aaaa
[-] Bad password... Try again.
```
Alright, let's open it in IDA to see what's going on. The main function is very simple:
```c
int __cdecl main(int argc, const char **argv, const char **envp){
  if ( argc == 2 ){
    if ( (unsigned int)check_password(argv[1]) )
      puts("[-] Bad password... Try again.");
    
    else
      puts("[+] Well done ! You can validate with flag :)");
    return 0;
  
  }else{
    printf("Usage: %s <flag>\n", *argv);
    return 1;
  }
}
```
So the interesting part is in the `check_password(char* password)` function. Let's check this out:
```c
__int64 __fastcall check_password(const char *password){
  int i; // [rsp+Ch] [rbp-4h]

  if ( strlen(password) == 33 ){
    for ( i = 0; i < 33; ++i ){
      if ( (password[i] ^ *(unsigned __int8 *)(i % 4 + 0x400000)) != (unsigned __int8)key[i] )
        return 1;
    }
    return 0;
  
  }else{
    return (unsigned int)-1;
  }
}
```
This is a simple XOR: our password XORed to the ELF magic bytes (at 0x400000 because the binary is not a PIE) must be equal to a hardcoded key. Let's dump the content of the `char key[33]` buffer and make a solving script in python.
```py
key = [
		0x37, 0x20, 0x3e, 0x29, 0x04, 0x09, 0x00,
		0x10, 0x32, 0x1a, 0x7d, 0x35, 0x20 ,0x71,
		0x13, 0x30, 0x4c, 0x37, 0x35, 0x19, 0x1c,
		0x75, 0x7c, 0x2a, 0x20, 0x35, 0x3e, 0x76,
		0x15,0x76,0x2f,0x32,0x02
	  ]

header = [0x7f, ord('E'), ord('L'), ord('F')]
flag = ""

for i in range(33):
	flag += chr(key[i] ^ header[i%4])

print(f"[+] Flag: {flag}")
```
Result:
```bash
$ python3 solve.py 
[+] Flag: Hero{LLVM_1s_4_v3ry_c00l_pr0j3ct}
```

### Flag

```
Hero{LLVM_1s_4_v3ry_c00l_pr0j3ct}
```
