from gpiozero import Button
from board import D18
from neopixel import NeoPixel
from random import choice
from time import sleep
from os import system
from json import load

# system('cd /home/pi/Desktop/TUESFest2019')
# o = load(open("/home/pi/Desktop/TUESFest2019/Comp_questions.json","r"))
pixels = NeoPixel(D18, 16)
while True:
    for i in range(16):
        pixels[i] = choice([(255,0,50),(0,255,0),(0,0,255),(200,200,200)])
    sleep(0.5)
# pixels[1] = (50,255,255)
# pixels[2] = (50,255,100)
# pixels[3] = (0,200,220)
pixels.fill((0,0,0))

# pixels[0] = (50,40,30)
# pixels.fill((0,0,0))

jacks_pins = [
    13,
    22,
    6,
    8,
    3,
    10,
    20,
    27,
    19,
    24,
    23,
    25,
    16,
    # 21, # на късо свързано и винаги е pushed state - hardware error
    12,
    9
]

jacks_repr = {
    13:"I",
    22:"II",
    6:"III",
    8:"IV",
    3:"V",
    10:"VI",
    20:"VII",
    27:"VIII",
    19:"IX",
    24:"X",
    23:"XI",
    25:"XII",
    16:"XIII",
    21:"XIV", # на късо свързано и винаги е pushed state - hardware error
    12:"XV",
    9:"XVI",
    # Buttons
    2:"Middle Button",
    26:"Black Button",
    17:"Red Button"

}

#
# while True:
#     try:
#         for i in jacks_pins:
#             if Button(i).is_pressed:
#                 print("pressed {}".format(jacks_repr[i]))
#     except RuntimeError as e:
#         print(e)
#         continue
#     except SegmentationFault as e:
#         print(e)
#         continue
#     sleep(2)
