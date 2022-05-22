import wave, sys

# Parse arguments
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input_file>")
    sys.exit(1)

stereo_file = None
try:
    stereo_file = wave.open(sys.argv[1], "rb")
    if stereo_file.getnchannels() != 2:
        print(f"[!] {sys.argv[1]} is not a stereo file")
        sys.exit(1)
except:
    print(f"[!] Could not open {sys.argv[1]} as wav file")
    sys.exit(1)


print(f"[+] Reading {stereo_file.getnframes()} frames and ordering by channel")
data = [[-1, -1]]
for i in range(stereo_file.getnframes()):
    f = stereo_file.readframes(1)
    if f != b"\x00\x00\x00\x00":
        if f[:2] == b"\x00\x00":
            if data[-1][0] == 0:
                data[-1][1] += 1
            else:
                data.append([0, 1])
        else:
            if data[-1][0] == 1:
                data[-1][1] += 1
            else:
                data.append([1, 1])
data = data[1:]


print(f"[+] Attempting to detect smallest chunk to assign bit size")
bit_size = min(data, key=lambda x: x[1])[1]


print(f"[+] Decoding text")
binary = ""
for d in data:
    binary += str(d[0]) * (d[1]//bit_size)
text = ""
for i in range(0, len(binary), 8):
    text += chr(int(binary[i:i+8], 2))


print(f"[+] Decoded text: {text}")