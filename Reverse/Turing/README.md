# Turing

### Category

Reverse

### Description

A strange character approaches you and whispers in your ear «Hey did you know that the mov instruction was Turing complete?».
He then slips a USB stick with a strange binary on it into your pocket.

Can you solve his riddle?


Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [Turing](Turing)

### Write up

This challenge was created with the `movfuscator` (see the git submodule in this folder). It's a pretty famous project and a guy has developped a `demovfuscator` project that you will also find in this directory.

The first step was to compile this demovfuscator and for this, to me, there was 3 important steps:
- fix the code following this issue: [https://github.com/kirschju/demovfuscator/pull/23/commits/f25b112e2aa1666594dff1c0a6df6d5ad5cd7ed0](https://github.com/kirschju/demovfuscator/pull/23/commits/f25b112e2aa1666594dff1c0a6df6d5ad5cd7ed0)
- Compile the keystone project to have the libs
- Compile the movfuscator (lol)

After applying the demovfuscator on the challenge, we can launch it to see how it works:
```bash
$ ./Turing_deobfuscated 
usage: ./Turing_deobfuscated <flag>
$ ./Turing_deobfuscated 1234
[-] Nope.
$ ./Turing_deobfuscated 1234 1234
usage: ./Turing_deobfuscated <flag>
```
So we need to provide the flag as a parameter and only one parameter. So in the code it must have a comparison between argc and 1.

We can see many conditionnal jump after the test of the `b0` register: it will help to see the comparison blocks.

So, the first block will compare argc to 2 so let's see where i putted 2 to understand the comparison blocks:
```c
  alu_x = R3;
  alu_y = 2;
  alu_t = 2;
```

We can see that the compared value is putted is those registers. Following this method, we can see that the flag is compared byte per byte to values:
```c
alu_x = R1;
alu_y = 'I';
alu_t = 'I';
```
...
```c
R2 = '!';
branch_temp = 0x8804E61B;
alu_x = R3;
alu_y = '!';
alu_t = '!';
alu_c = 1;
```

Final flag after byte per byte comparison: `Hero{I_l1k3_t0_m0v3_1t!}`

(sorry for the bad write-up quality, I'm drunk <3 but I hope you've liked the CTF)

### Flag

```
Hero{I_l1k3_t0_m0v3_1t!}
```
