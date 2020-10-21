from gpiozero import Button
from board import D18
from neopixel import NeoPixel
import time
import numpy
# import threading
from random import randint, choice
# import pdb

pixels = NeoPixel(D18, 16)
pixels.fill((0, 0, 0))
# global jacks_pins 

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
    11,
    12,
    9
]

jacks_diodes = {
    12: 15,
    9: 14,
    13: 13,
    22: 12,
    6: 11,
    8: 10,
    3: 9,
    10: 8,
    20: 7,
    27: 6,
    19: 5,
    24: 4,
    23: 3,
    25: 2,
    16: 1,
    11: 0
}

jacks_repr = {
    13: "I",
    22: "II",
    6: "III",
    8: "IV",
    3: "V",
    10: "VI",
    20: "VII",
    27: "VIII",
    19: "IX",
    24: "X",
    23: "XI",
    25: "XII",
    16: "XIII",
    11: "XIV",
    12: "XV",
    9: "XVI",
    # Buttons
    2: "Middle Button",
    26: "Black Button",
    17: "Red Button"
}


global colors
colors = {
    'Game': (50, 40, 30),
    'Black': (0, 0, 0),
    'Wrong': (50, 255, 255),
    'Goto': (0, 255, 255),
    'Start': (200, 200, 200),
    'Green': (255, 0, 0),
    'Red': (0, 255, 0),
    'Blue': (0, 0, 255)
}

scaleSwitch = {
    0.1: "Hard",
    0.3: "Medium",
    0.5: "Easy"
}


def START_CHECK():  # works fine
    '''
    no input
    no return value
    checks which fields are in use and asks to be freed
    '''
    global pixels, jacks_pins, jacks_diodes, colors
    j = 0
    while j != len(jacks_pins):
        j = 0
        for i in jacks_pins:
            try:
                if Button(i).is_pressed:
                    print("Pull out palm on {} field".format(jacks_repr[i]))
                    pixels[jacks_diodes[i]] = colors['Wrong']
                    Button(i).wait_for_release()
                    pixels[jacks_diodes[i]] = colors['Black']
                j += 1
            except RuntimeError:
                continue


def get_pin(curr_pin_indx):
    '''
    input int index of current pos in jacks_pins
    output int next position as field
    '''
    a = randint(6, 8)
    ret = 0
    if (curr_pin_indx + a) >= len(jacks_pins):
        ret = jacks_pins[(curr_pin_indx + a) - len(jacks_pins)]
    else:
        ret = jacks_pins[curr_pin_indx + a]
    return ret


def LED_START(end='Start'):
    '''
    input no/color to show after 'show'
    output none
    '''
    global pixels
    for _ in range(5):
        for i in range(len(jacks_pins)):
            pixels[jacks_diodes[jacks_pins[i]]] = choice(list(colors.values()))

            time.sleep(0.01)
    pixels.fill(colors[end])


def winner(who=0):
    '''
    input winnter, by default player lost
    output console print
    '''
    if who:
        print("Player won")
        return 1
    else:
        print("Player lost")
        return 0


def snake(to_go, now_indx, delay, scale=0.4):
    '''
    moves the 'snake' and stops when:
        1) player 'eats the apple'
        2) snake 'eats the apple'
    input
            (int) to_go next position
            (int) now_indx index of current position
            (float) delay time to wait
    output none
    '''
    global pixels, jacks_diodes, jacks_pins, colors
    flag = 0  # 1 -> player won | 0 -> player lost
    delay *= 2 / 10
    # pdb.set_trace()
    if now_indx < to_go:
        for i in jacks_pins[now_indx:to_go+1]:
            pixels[jacks_diodes[i]] = colors["Green"]
            if Button(jacks_pins[to_go]).is_pressed:
                flag = winner(1)
                return flag
            if delay >= 0:
                time.sleep(scale - (delay))
        return winner(0)
    else:
        for i in jacks_pins[now_indx:]:
            pixels[jacks_diodes[i]] = colors["Green"]
            if Button(jacks_pins[to_go]).is_pressed:
                flag = winner(1)
                return flag
            if delay >= 0:
                time.sleep(scale - (delay))
        if flag:
            return 1
        else:
            for i in jacks_pins[:to_go]:
                pixels[jacks_diodes[i]] = colors["Green"]
                if Button(jacks_pins[to_go]).is_pressed:
                    flag = winner(1)
                    return 1
                if delay >= 0:
                    time.sleep(scale - (delay))
            return winner(0)
    return 1


def start(scale, start_field_pin=13):
    # START_CHECK()  # Clears the board
    pixels[jacks_diodes[start_field_pin]] = colors['Blue']  # Lights the first

    Button(start_field_pin).wait_for_press()  # wait for press on first

    now_indx = jacks_pins.index(start_field_pin)  # index of starting field
    win = 0
    for i in numpy.arange(0, 4.0, 0.01):  # 40 levels, could be more or less
        print("level {}".format(int(i*100)))
        to_go = get_pin(now_indx)  # returns a next random field

        pixels[jacks_diodes[jacks_pins[now_indx]]] = colors["Red"]

        Button(jacks_pins[now_indx]).wait_for_release()

        pixels[jacks_diodes[to_go]] = colors["Game"]  # Lights the next field

        win = snake(
            to_go=jacks_pins.index(to_go),
            now_indx=now_indx,
            delay=i,
            scale=scale
        )

        pixels.fill(colors['Black'])  # resets the colors

        if not win:
            print(
                "Sorry you lost on level {lvl} and {scl} level scale".format(
                    lvl=int(i*100)+1, scl=scaleSwitch[scale]
                )
            )
            break

        now_indx = jacks_pins.index(to_go)  # gets the new index of curr_pos


if __name__ == "__main__":
    # pixels.brightness = 0.8
    start_field_pin = 13
    scale = 1.2
    while 1:
        LED_START(end="Start")

        print("Level Scale?\nRed - Hard\nGreen - Medium\nBlue - easy")
        pixels[jacks_diodes[13]] = colors["Red"]
        pixels[jacks_diodes[22]] = colors["Green"]
        pixels[jacks_diodes[6]] = colors["Blue"]
        while 1:
            if Button(13).is_pressed:
                scale = 0.1
                start_field_pin = 13
                break
            elif Button(22).is_pressed:
                scale = 0.3
                start_field_pin = 22
                break
            elif Button(6).is_pressed:
                scale = 0.5
                start_field_pin = 6
                break
        
        LED_START(end="Black")
        start(scale=scale, start_field_pin=start_field_pin)
        # print("Well done, you just won!")

        LED_START(end="Black")
        print("If you want to play again click the Black button, \
else - the red")

        while 1:
            if Button(26).is_pressed:
                break
            elif Button(17).is_pressed:
                print("Bye")
                exit(1)
