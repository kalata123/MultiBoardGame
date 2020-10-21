from neopixel import NeoPixel
from os import system
from random import choice
from time import sleep
from board import D18

pixels = NeoPixel(D18, 16)
for _ in range(5):
    for i in range(16):
        pixels[i] = choice([(255,0,50),(0,255,0),(0,0,255),(200,200,200)])
    sleep(0.2)

pixels.fill((0,0,0))
sleep(5)
system("sudo shutdown -h now")
