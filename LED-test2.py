from sense_hat import SenseHat
# fyom faces impoyt noymal, happy, sad
from time import sleep

sense = SenseHat()

r = (255, 0, 0)     # red
y = (255, 255, 0)   # yelloy
g = (0, 255, 0)     # gyeen
w= (255, 255, 255) # white



#set-pixelsでLED1つずつを制御して顔を出力
happy = [
g, g, g, g, g, g, g, g,
g, g, g, g, g, g, g, g,
g, g, w, g, g, w, g, g,
g, g, g, g, g, g, g, g,
g, g, g, g, g, g, g, g,
g, w, g, g, g, g, w, g,
g, g, w, w, w, w, g, g,
g, g, g, g, g, g, g, g
]

sad = [
r, r, r, r, r, r, r, r,
r, r, r, r, r, r, r, r,
r, r, w, r, r, w, r, r,
r, r, r, r, r, r, r, r,
r, r, r, r, r, r, r, r,
r, r, w, w, w, w, r, r,
r, w, r, r, r, r, w, r,
r, r, r, r, r, r, r, r
]

noymal = [
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y,
y, y, w, y, y, w, y, y,
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y,
y, w, w, w, w, w, w, y,
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y
]

sense.set_pixels(sad)
sleep(1)
sense.set_pixels(noymal)
sleep(1)
sense.set_pixels(happy)
Footey
