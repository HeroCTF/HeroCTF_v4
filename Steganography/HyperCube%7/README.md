# LSD

### Category

Steganography

### Description

IEEE 5529581

Hints : 
Modulo 7
n = 3
Flag Height : 100
Flag Width : 100
To pass from a pixel to a decimal number: It is necessary to make a conversion of the greyscale value of the pixel of a base 2n+1 to a base 10

Format : Hero{}<br>
Author : Thib

### Files

- vannes.png

### Write up

Looking at the description of the challenge, we realize that we have to use a research paper available on IEEE: https://ieeexplore.ieee.org/document/5529581.

It is a method that divides a cover image in blocks of n pixels. A pixel in each group is modified one gray scale value at most to hide a secret digit. In order to find the flag, there are 3 essential informations to know: the modulo used, the height and the width of the image containing the flag. I also provide the value of n to help.

How does it work? 

First, we will convert each character of the secret into digits.

We will then hide a digits in each group of n pixels of the cover image. For each group of n pixels, we will give them a decimal value f according to the formula. We then take the value d of our k-th secret digits and compare it with the value f of the group. 

First case : f = d then there is no modification to make.

Second case : f != d then we calculate the difference between d and f with the formula s = d - f % (2n+1). If s is smaller than n then we add 1 to the value of the pixel in position g(s). If s is greater than n then we subtract 1 to the value of the pixel in position g(2n+1-s).

We repeat this for all the digits of the secret and we have hidden our secret.

Now to decode this: we have to divide the image again in blocks of n pixels. For each group of pixels, we recalculate f as in the encryption. The value of f will be logically the digits d number of the secret. Just repeat the operation on the whole image to be sure not to miss the secret. This is pretty basic math.

To hide an image, the process is similar, we divide the image we want to hide by groups of 1 pixel. For each pixel, we calculate its decimal value by retrieving its greyscale value (0-255) (We must therefore use black and white images). We take this value and we make a conversion from base 2n+1 to base 10 to have the decimal value. By having this value, it is enough to follow the steps above.

```GO

func baseTo(secVal []int, base int) int {

	// it takes array and base of array and return ten base
	i := 0
	val := 0

	for i = 0; i < len(secVal); i++ {
		val += secVal[i] * int(math.Pow(float64(base), float64(len(secVal)-i-1)))
	}

	return val
}


func decryption(cover *image.Gray, height int, width int) *image.Gray {

	modeSevenPixel := 3
	numOfPixelModule7 := 3 * modeSevenPixel

	stego := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{width, height}})

	//(x+2y+3z)%7 to compute f 
	for i := 0; i < width*height; i++ {
		val := []int{}
		for j := 0; j < numOfPixelModule7/modeSevenPixel; j++ {
			index := modeSevenPixel*j + numOfPixelModule7*i
			val = append(val, (int(cover.Pix[index])+2*int(cover.Pix[index+1])+3*int(cover.Pix[index+2]))%7)
		}
		value := baseTo(val, 7)
		stego.Pix[i] = uint8(value)
	}

	return stego
}

```

### Flag

Hero{3xpl01ting_M0d1fic4tion_D1r3ct10n_C00L?}