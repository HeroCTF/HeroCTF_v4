from PIL import Image

img1 = Image.open("embeder.png")
img2 = Image.open("poney.png")

x1, y1 = img1.size
img2 = img2.resize((500, 750))
x2, y2 = img2.size

image = Image.new('RGB', (x1+x2, y1))
image_map = image.load()

output = ""
for y in range(y1):
    c1x = 0
    c2x = 0
    for x in range(x1+x2):    
        if x%7 != 0:
            image_map[x, y] = img1.getpixel((c1x, y))
            output += ",".join(list(map(str, img1.getpixel((c1x, y))))[:3]) + "-"
            c1x += 1
        elif y%2 == 0:
            image_map[x, y] = img2.getpixel((c2x, int(y/2)))
            output += ",".join(list(map(str, img2.getpixel((c2x, int(y/2)))))[:3]) + "-"
            c2x += 1
        else:
            image_map[x, y] = (255,255,255)
            output += "0,0,0-"
        

open("input.txt", "w").write(output[:-1])
image.save("embeded.png")