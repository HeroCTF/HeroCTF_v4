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
