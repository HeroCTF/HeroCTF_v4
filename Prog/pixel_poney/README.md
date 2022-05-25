# Pixel Poney

### Category

Prog

### Description
I'm not in a mood of writing riddles as an explanation for this challenge, so I'm gonna be straight with you. Those numbers in the input file represent pixels, and the image you seek has a width of 3500 pixels. See ya

Format : **Hero{flag}**<br>
Author : **Log_s**

### Files

 - [input.txt](input.txt)

### Write up

Ok, so we know we have to reconstruct an image, and that its size is 3500x????.

Let's determine the size, by loading all the pixel values in an array, and calculate the missing height.

```python
# Read pixels from input file
pixels = open("input.txt", "r").read().split("-")

# Determine height based on the known width
width = 3500
height = int(len(pixels)/width)
```

Now let's create a blank image of the right size. We'll also load the corresponding array, that contains the pixel values, in `image_map`.
```python
image = Image.new('RGB', (width, height))
image_map = image.load()
```

Finally let's loop through our pixels, and paste them on the image.
```python
for y in range(height):
    for x in range(width):
        image_map[x, y] = tuple(map(int, pixels[x+(y * width)].split(',')))
```
The only part that may be a problem to understand is this part : `tuple(map(int, pixels[x+(y * width)].split(',')))`. We basically get the pixel input using `x+(y*width)` that looks like this `'255,255,255'`, split it to obtain a list `['255', '255', '255']`, apply `int()` on every member of the array using `map()` and converting the iterable it produces to a tuple, obtaining this `(255, 255, 255)`.

We can either show the image with `image.show()` or save it using `image.save("out.png")`.

But wait ?? What is this...

![](embeded.png)

There is no flag here, but an indication: "Take a better look at the pixels". When zooming in with gimp for exemple, we notice strange pixel columns. There is one wierd column every 6 normal ones. Every wierd column is made of an alternation of white pixels and some other color.

If we take a look at the bottom right of the image, we can decipher `ero` on the green part.

There is another image embeded in this one !

Let's take only the wierd looking columns (every 7th column then), and leave out the white pixels.

We can reuse the previous script, and only change the images size, and add a condition to paste the pixel.

Here is the final script.

```python
from PIL import Image

# Read pixels from input file
pixels = open("input.txt", "r").read().split("-")

# Determine height based on the known width
width = 3500
height = int(len(pixels)/width)

# Create blank image of size width/2 x height/2
image = Image.new('RGB', (int(width/7), int(height/2)))
image_map = image.load()

for y in range(height):
    for x in range(width):
        # Load only every two lines and every 7 pixels
        if x%7 == 0 and y%2 == 0:
            image_map[int(x/7), int(y/2)] = tuple(map(int, pixels[x+(y * width)].split(',')))

image.show()
```

Congratz, here is your poney ;)

![](poney.png)

### Flag

```Hero{So_You_reconStruKted_the_imAge_??}```