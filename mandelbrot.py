from PIL import Image

img = Image.new('RGB', (400, 400), color = 0)
pixels = img.load()

for x in range(img.size[0]):
    for y in range(img.size[1]):
        num = 0
        c = complex((x-300)/150,(y-200)/150)
        z = complex(0,0)
        for i in range(600):
            z = z**2+c
            if abs(z) > 2:
                num = i
                break
        g = int(num*255/600)
        pixels[x,y] = (g, g ,g)


img.save("mandelbrot.png")
