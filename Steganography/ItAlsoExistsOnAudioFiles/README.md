# LSD

### Category

Steganography

### Description

Did you know that wave files are composed of frames?? It opens the field of possibilities!

Format : **Hero{}**<br>
Author : **Thib**

### Files

- [Song](song.wav)

### Write up

Looking at the title, one can guess that a steganography method normally used for images must be used. Moreover the statement of the challenge speaks to us about frames. We can easily make the link between the pixels of an image and the frames of a .wav file! So let's use our dear LSB.

1. By doing some research, we realize that wave files can be decomposed into "frames" which can be decomposed into a sequence of bits. So we can modify the LSB of each frame to hide an image!

2. Python has a perfect library for what we want to do.

```python
def decodeLSBInWave(song):

    print("Decoding...")

    song = wave.open(song, mode='rb')
    #print("Reading file: "+song.getparams()[0])

    # Convert audio to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    # Extract the LSB of each byte
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    #print("Extracted bits: "+str(extracted))

    # Convert byte array back to string
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    
    # Cut off at the filler characters
    decoded = string.split("###")[0]

    # Print the extracted text
    print("Sucessfully decoded: "+decoded)
    song.close()

```


### Flag
```
Hero{L5B_0N_4UD10}
```