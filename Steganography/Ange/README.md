# Ange

### Category

Steganography

### Description

Everyting is in the title !

Format : Hero{}<br>
Author : Thib

### Files

- redactedFinal.png

### Write up

It is a challenge inspired by a researcher: Ange Albertini (https://twitter.com/angealbertini)

The principle is to encrypt an image in AES to obtain another totally valid image.

By using foremost on the image, we discover a barcode that provides us with a key and an IV. It is enough to apply an AES encryption on the basic image to obtain another image.

- Key : thisisjustakeyyy
- IV : \x7a\xeb\x7e\x7a\x02\xa5\x7f\x77\x40\xfd\xc1\x6d\x6f\xfa\x79\xe7

Then in the upper left corner there is the flag. We can use Stegsolve or aperisolve to discover it.


### Flag

Hero{4NG3_4L83R71N1}