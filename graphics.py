import cv2
import urllib.request
import numpy as np

from PIL import ImageFont, ImageDraw, Image

def graphics(data):
    SIZE = 180

    albums = [d[0] for d in data]
    artists = [d[1] for d in data]
    plays = [d[2] for d in data]
    imgs = [d[3] for d in data]

    img = 255 * np.ones((SIZE*5, SIZE*5, 3), dtype = np.uint8)

    counter = 0
    for y in range(5):
        for x in range(5):
            if imgs[counter]:
                req = urllib.request.urlopen(imgs[counter])
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                pic = cv2.imdecode(arr, cv2.IMREAD_COLOR) # 'Load it as it is'
                pic = cv2.resize(pic, (SIZE,SIZE), interpolation = cv2.INTER_AREA)

                try:
                    img[y*SIZE:(y+1)*SIZE,x*SIZE:(x+1)*SIZE] = pic[0:SIZE,0:SIZE]
                except:
                    pic = pic.reshape((pic.shape[0], pic.shape[1], 1))
                    img[y*SIZE:(y+1)*SIZE,x*SIZE:(x+1)*SIZE] = pic[0:SIZE,0:SIZE]

                black_strip = np.zeros((int(SIZE/5), SIZE, 3))
                img[y*SIZE:int((y+.2)*SIZE), x*SIZE:(x+1)*SIZE] = (black_strip[::]+img[y*SIZE:int((y+.2)*SIZE), x*SIZE:(x+1)*SIZE])/2
            counter += 1

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)

    counter = 0
    for y in range(5):
        for x in range(5):
            text_size = int(SIZE / 12)
            if len(albums[counter]) > 22:
                text_size = int(22*text_size/len(albums[counter]))
            font = ImageFont.truetype("fonts/arialbold.ttf", text_size)
            draw.text((2 + x*SIZE, int((y+.03)*SIZE)), albums[counter], font=font, fill=(255, 255, 255), stroke_width=0)

            text_size = int(SIZE / 12)
            if len(artists[counter]) > 18:
                text_size = int(18*text_size/len(artists[counter]))
            font = ImageFont.truetype("fonts/cour.ttf", text_size)
            draw.text((2 + x*SIZE, y*SIZE + int(.2 * SIZE) - 3), artists[counter], font=font, fill=(255, 255, 255), anchor='lb')


            counter += 1
    
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()