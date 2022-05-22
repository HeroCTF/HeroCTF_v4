import wave, sys

# Parse arguments
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <input_file> <output_file> <text>")
    sys.exit(1)

mono_file, stereo_file, text = None, None, sys.argv[3]
try:
    mono_file = wave.open(sys.argv[1], "rb")
    if mono_file.getnchannels() != 1:
        print(f"[!] {sys.argv[1]} is not a mono file")
        sys.exit(1)
except:
    print(f"[!] Could not open {sys.argv[1]} as wav file")
    sys.exit(1)

try:
    stereo_file = wave.open(sys.argv[2], "wb")
except:
    print(f"[!] Could not open {sys.argv[2]} as wav file")
    sys.exit(1)


# Config output file
print(f"[+] Configuring output file {sys.argv[2]}")
stereo_file.setnchannels(2)
stereo_file.setsampwidth(mono_file.getsampwidth())
stereo_file.setframerate(mono_file.getframerate())


# Load and trim audio file
print(f"[+] Loading input file in memory and trimming")
started = False
in_frames = []
for _ in range(mono_file.getnframes()):
    f = mono_file.readframes(1)
    if f !=  b"\x00\x00":
        in_frames.append(f)


# Convert text to binary
binary = ""
for l in text:
    binary += bin(ord(l))[2:].zfill(8)


# Encode text
bit_size = len(in_frames) // len(binary)

print(f"[+] Encoding {len(binary)} bits into {len(in_frames)} frames")
frame_counter = 0
for bit in binary:
    for _ in range(bit_size):
        f = in_frames[frame_counter]
        if bit == "1":
            stereo_file.writeframes(f)
            stereo_file.writeframes(b"\x00\x00")
        else:
            stereo_file.writeframes(b"\x00\x00")
            stereo_file.writeframes(f)
        frame_counter += 1

print(f"[+] Encoding complete")

mono_file.close()
stereo_file.close()

