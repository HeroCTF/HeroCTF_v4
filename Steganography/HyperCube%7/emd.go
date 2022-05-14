package main

import (
	"image"
	"image/color"
	"image/png"
	"math"
	"os"
)

func readImage(path string) image.Image {
	infile, err := os.Open(path)
	if err != nil {
		panic(err.Error())
	}
	defer infile.Close()

	src, _, err := image.Decode(infile)
	if err != nil {
		panic(err.Error())
	}
	return src
}

func rgbToGray(im image.Image) *image.Gray {

	bounds := im.Bounds()
	width, height := bounds.Max.X, bounds.Max.Y
	gray := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{width, height}})

	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {

			oldColor := im.At(x, y)
			r, g, b, _ := oldColor.RGBA()
			avg := (float64(r) + float64(g) + float64(b)) / 3
			var grayColor color.Gray
			grayColor = color.Gray{uint8(avg / 256)}
			gray.Set(x, y, grayColor)
		}
	}

	return gray
}

func writeImage(im image.Image, imName string) {

	outfile, err := os.Create(imName)
	if err != nil {
		panic(err.Error())
	}
	defer outfile.Close()
	png.Encode(outfile, im)
}

func reverseArray(numbers []int) []int {

	for i, j := 0, len(numbers)-1; i < j; i, j = i+1, j-1 {
		numbers[i], numbers[j] = numbers[j], numbers[i]
	}
	return numbers
}

func toBase(val int, base int) []int {

	// (11,5) -> number 11 to base five
	// it returns [2, 1]
	temp := []int{}
	for true {
		temp = append(temp, val%base)
		if val >= base {

			val /= base
		} else {

			break
		}
	}
	return reverseArray(temp)
}

func baseTo(secVal []int, base int) int {

	// it takes array and base of array and return ten base
	i := 0
	val := 0

	for i = 0; i < len(secVal); i++ {
		val += secVal[i] * int(math.Pow(float64(base), float64(len(secVal)-i-1)))
	}

	return val
}

func encryption(cover *image.Gray, stego *image.Gray) *image.Gray {

	modeSevenPixel := 3
	numOfPixelModule7 := 3 * modeSevenPixel

	coverBounds := cover.Bounds()
	//cover image width and height
	coverW, coverH := coverBounds.Max.X, coverBounds.Max.Y

	coverAfter := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{coverW, coverH}})

	for i := 0; i < coverW*coverH; i++ {

		if cover.Pix[i] == 255 {
			cover.Pix[i] = 254
		} else if cover.Pix[i] == 0 {
			cover.Pix[i] = 1
		}
		coverAfter.Pix[i] = cover.Pix[i]
	}

	stegoBounds := stego.Bounds()
	//stego image width and height
	stegoW, stegoH := stegoBounds.Max.X, stegoBounds.Max.Y
	//if mode is 0 then use module 5 for encryption
	//if mode is 1 then use module 7 for encryption
	//if mode is -1, can't encrypt

	//(x+2y+3z)%7
	for i := 0; i < stegoW*stegoH; i++ {
		secVal := toBase(int(stego.Pix[i]), 7)
		//how many zeros will be added before the number
		numZeros := numOfPixelModule7/modeSevenPixel - len(secVal)
		for j := 0; j < numOfPixelModule7/modeSevenPixel; j++ {
			//index starts with 18, after 18 pixel header
			index := modeSevenPixel*j + numOfPixelModule7*i
			val := int(int(coverAfter.Pix[index])+2*int(coverAfter.Pix[index+1])+3*int(coverAfter.Pix[index+2])) % 7
			diff := 0
			if j < numZeros {
				diff = val
			} else {
				diff = val - secVal[j-numZeros]
			}
			if (diff == -6) || (diff == 1) {
				coverAfter.Pix[index] -= 1
			} else if (diff == -5) || (diff == 2) {
				coverAfter.Pix[index+1] -= 1
			} else if (diff == -4) || (diff == 3) {
				coverAfter.Pix[index+2] -= 1
			} else if (diff == -3) || (diff == 4) {
				coverAfter.Pix[index+2] += 1
			} else if (diff == -2) || (diff == 5) {
				coverAfter.Pix[index+1] += 1
			} else if (diff == -1) || (diff == 6) {
				coverAfter.Pix[index] += 1
			}
		}
	}

	return coverAfter
}

func decryption(cover *image.Gray, height int, width int) *image.Gray {

	//numbers from 0 to 255 can represent 3 digits in module 7
	//x+2y+3z(3 pixel) and 3 digits
	modeSevenPixel := 3
	//9 cover pixels for 1 stego pixel
	numOfPixelModule7 := 3 * modeSevenPixel

	stego := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{width, height}})

	//(x+2y+3z)%7
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

func main() {

	writeImage(encryption(rgbToGray(readImage("coverGrey.png")), rgbToGray(readImage("flagGrey.png"))), "output.png")
	writeImage(decryption(rgbToGray(readImage("output.png")), 100, 100), "outputFlag.png")

}
