# LSD

### Category

Steganography

### Description

Don't try to throw random tools at this poor image. Go back to the basics and learn the detection techniques.

Format : **Hero{}**<br>
Author : **Thib**

### Files

- [secret](secret.png)

### Write up

Through this challenge, I wanted to force the players to understand how the LSB works rather than just throwing random bruteforce tools.

1. By playing a little with the contrast of the image, we realize that there is a diagonal line of pixels that is quite strange: it is a diagonal LSB!

2. Simply iterate over all the diagonal pixels of the image and concatenate the bits of the three RGB(A) channels

```python
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


def stringToBinary(string):
    return ''.join([format(ord(i), "08b") for i in string])
```


### Flag
```
Hero{L5B_D14G_0R1G1N4L_N0P_?}
```