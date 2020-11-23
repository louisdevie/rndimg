# pygame imports
from pygame import *
from pygame.locals import *

# stdlib imports
import requests
import random
import os

# directory of the app
localdir = os.path.dirname(os.path.abspath(__file__))
print(localdir)

chars = 'abcdefghijklmnopqrstuvwxyz'

# there's two methods used to get random images:
# 1) sequence of 3 to 6 random letters
def rndseq():
    seq = ''
    for i in range(random.randint(3, 6)):
        seq += random.choice(chars)
    return seq

# 2) the same letter repeated between 6 and 20 times
def rptseq():
    return random.choice(chars)*random.randint(6, 20)

# search on qwant and download a random one from the first 50
def getimg():
    while True:
        query = random.choice((rndseq, rptseq))()

        r = requests.get("https://api.qwant.com/api/search/images",
            params={
                'count': 50,
                'q': query,
                't': 'images',
                'safesearch': 0,
                'locale': 'fr_FR',
                'uiv': 4
            },
            headers={
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
          }
        )

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]
        if urls:
            url = random.choice(urls)

            print(url)
            response = requests.get(url)
            ext = url.split('.')[-1]
            path = "%s\\rndimg.%s" % (localdir, ext)

            file = open(path, "wb")
            file.write(response.content)
            file.close()
            return path
        print('no images found')

# display the new img
def newimg():
    try:
        window.fill((0, 0, 0))
        window.blit(lbl, pos)
        display.flip()
        print('cleared')
        p = getimg()
        img = image.load(p)
        w, h = img.get_size()
        print('img loaded (w: %i, h: %i)' %(w, h))
        if w > 1000 or h > 600:
            r = min(1000/w, 700/h)
            w, h = int(w*r), int(h*r)
            img = transform.smoothscale(img, (w, h))
            print('img resized (w: %i, h: %i)' %(w, h))
        x, y = 500 - int(w/2), 300 - int(h/2)
        window.blit(img, (x, y))
        display.flip()
        print('img displayed')
    except BaseException as err:
        print('error %r, cancel' %err)

# pygame setup stuff i dunno
init()

running = True
searching = False
clock = time.Clock()
display.set_caption('Random image')
window = display.set_mode((1000, 600))

fnt = font.SysFont('Calibri', 20)
lbl = fnt.render('Click anywhere or press [ENTER] to search for a new random image', 1, (255, 255, 255))
w, h = lbl.get_size()
pos = int(500 - w/2), int(300-h)
window.blit(lbl, pos)
lbl = fnt.render('powered by QWANT', 1, (255, 255, 255))
w, h = lbl.get_size()
pos = int(500 - w/2), 300
window.blit(lbl, pos)
display.flip()
lbl = fnt.render('Searching new ...', 1, (255, 255, 255))
w, h = lbl.get_size()
pos = int(500 - w/2), int(300-h/2)

while running:
    for ev in event.get():
        if ev.type == QUIT:
            running = False
        elif ev.type == MOUSEBUTTONUP:
            if ev.button == 1:
                newimg()
        elif ev.type == KEYUP:
            if ev.key == K_RETURN:
                newimg()

    clock.tick(33)

quit()
