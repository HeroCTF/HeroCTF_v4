from PIL import Image
import numpy as np
from math import *

def createWhitePictureWithPIL(width, height):
    img = Image.new('RGB', (width, height), color = 'white')
    img.save('whiteDefault.png')
    return img

def stringToBinary(string):
    return ''.join([format(ord(i), "08b") for i in string])

def binaryArrayToString(binary):
    string_ints = [str(int) for int in binary]
    str_of_ints = "".join(string_ints)
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(str_of_ints), 8)])

def binaryToString(binary):
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])

def encode(src, data):
    print("[-] Encoding... ")
    img = Image.open(src, 'r')
    width, height = img.size
    if width != height:
        print("[-] Error: Image is not square!")
        exit()
    
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        mode = 3
        print("[-] RGB mode")
    elif img.mode == 'RGBA':
        mode = 4
        print("[-] RGBA mode")

    total_pixels = width
    print("[-] Total pixels where information can be hide: {} pixels".format(total_pixels))
    
    maximumSizeMessage = total_pixels * mode
    print("[-] Maximum size of message: {} bits".format(maximumSizeMessage))

    bits_message = stringToBinary(data)
    print("[-] Message size in bits: {} bits".format(len(bits_message)))
    print("[-] Message in bits: {}".format(bits_message))

    if len(bits_message) > maximumSizeMessage:
        print("[-] ERROR : Message is too big to be hide in the image :(")
        exit()
    else:
        print("[-] The is enough space to hide the message !")
    i = 0
    for x in range(0, width):
        pixel = list(img.getpixel((x, x)))
        for n in range(0, mode):
            if (i < len(bits_message)):
                pixel[n] = pixel[n] & ~1 | int(bits_message[i])
                i  = i + 1
            img.putpixel((x, x), tuple(pixel))
            
    print("[-] Exact message which will be encoded: {}".format(binaryToString(bits_message)))
    print("[-] Message encoded !")
    print("[-] Saving image...")
    print("[-] Done ! Image saved as secret.png")
    img.save("secret.png", "PNG")

def decode(src):
    print("[-] Decoding... ")
    
    extracted_bin = ""
    img = Image.open(src, 'r')
    if img.mode == 'RGB':
        mode = 3
        print("[-] RGB mode")
    elif img.mode == 'RGBA':
        mode = 4
        print("[-] RGBA mode")
    width, height = img.size
    print("[-] Image size: {}x{}".format(width, height))
    for i in range(0, width):
        pixel = list(img.getpixel((i, i)))
        for n in range(0,mode):
            extracted_bin = extracted_bin + str((pixel[n]&1))
    print("[-] Message extracted in binary: {}".format(extracted_bin))
    print("[-] Message extracted in string: " + binaryToString(extracted_bin))

print("##########################################################")
print("######################## ENCODING ########################")
print("##########################################################")
encode('LSD.png', "Well done champ, you're starting to touch some real steganography. Glad you didn't just throw a random script. Here is your flag: Hero{L5B_D14G_0R1G1N4L_N0P_?}")
print("")

print("##########################################################")
print("######################## DECODING ########################")
print("##########################################################")
decode('secret.png')
