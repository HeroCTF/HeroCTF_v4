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