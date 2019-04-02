from gpiozero import Button
import time
from Classes import Player
import random
import board
from neopixel import NeoPixel

led_count = 16

pixels = NeoPixel(board.D18, led_count, auto_write=False)

colors = {
    "Yellow" : (70,75,0),
    'Blue' : (0,0,50),
    "Red" : (0,50,0),
    'Green' : (50,0,0),
    'Black': (0,0,0),
    'Wrong' : (0,255,255)
}

p1 = Player("Red",3,600,0)
p2 = Player("Yellow",3,600,1)
p3 = Player("Blue",3,600,2)
p4 = Player("Green",3,200,3)
total_players = 4
i = 0

jacks_diodes = {
    13:12,
    # 7:11,
    6:10,
    8:9,
    3:8,
    # 1:7,
    20:6,
    27:5,
    19:4,
    24:3,
    # 23:2,
    25:1,
    16:0,
    # 21:15,
    12:14,
    5:13
}

jacks_repr = {
    13:"I",
    # 7:"II", # на късо свързано и винаги е pushed state - hardware error
    6:"III",
    8:"IV",
    3:"V",
    # 1:"VI", # трябва да се оправи
    20:"VII",
    27:"VIII",
    19:"IX",
    24:"X",
    # 23:"XI",
    25:"XII",
    16:"XIII",
    # 21:"XIV", # на късо свързано и винаги е pushed state - hardware error
    12:"XV",
    5:"XVI",
    # Buttons
    2:"Black Button",
    26:"Blue Button",
    17:"Red Button"

}

jacks_pins = [
    13,
    # 7, # на късо свързано и винаги е pushed state - hardware error
    6,
    8,
    3,
    # 1,
    20,
    27,
    19,
    24,
    # 23,
    25,
    16,
    # 21, # на късо свързано и винаги е pushed state - hardware error
    12,
    5
]

buttons_pins = [
    26,
    2,
    17
]

neighbours = []
# LED Functions
def LED_START():
    for i in range(0,led_count-4,4):
        # pixels[i] = random.choice(list(colors.values()))
        pixels[jacks_diodes[jacks_pins[i]]] = list(colors.values())[0]
        pixels[jacks_diodes[jacks_pins[i+1]]] = list(colors.values())[1]
        pixels[jacks_diodes[jacks_pins[i+2]]] = list(colors.values())[2]
        pixels[jacks_diodes[jacks_pins[i+3]]] = list(colors.values())[3]
        # pixels[11] = (0,0,0)
        # pixels[7] = (0,0,0)
        # pixels[2] = (0,0,0)
        # pixels[15] = (0,0,0)
    pixels.show()
    time.sleep(1)

    for i in range(led_count):
        pixels[i] = colors['Black']
    pixels.show()
    time.sleep(0.1)


# Functions for beggining
def START_CHECK():
    # checks if the board is clear from palms
    j = 0
    while j is not len(jacks_repr.keys()) - 3:
        j = 0
        for i in jacks_pins:
            try:
                if Button(i).is_pressed:
                    print("Take out {} palm".format(jacks_repr[i]))
                    Button(i).wait_for_release()
                j += 1
            except RuntimeError as e:
                print(e)

def DICE_1():
    # returns a random pin number from jacks_pins list
    a = random.choice(jacks_pins)
    if a not in neighbours:
        return a
    return DICE_1()

def BUY(player, pos, money_to_pay = 100):
    # gives <pos> over to <player> and
    # changes <player>'s curr_position
    global pixels
    if player == 0:
        return p1.ADD_POSITION(pos, money_to_pay)
    elif player == 1:
        return p2.ADD_POSITION(pos, money_to_pay)
    elif player == 2:
        return p3.ADD_POSITION(pos, money_to_pay)
    elif player == 3:
        return p4.ADD_POSITION(pos, money_to_pay)

def LAST_POS(player):
    switch = {
        0:p1.curr_position,
        1:p2.curr_position,
        2:p3.curr_position,
        3:p4.curr_position
    }
    return switch[player]

def GO_BACK(player):
    print("You don't have enough money to buy this position\nPlease go back to {}"\
    .format(jacks_repr[LAST_POS(player)]))
    if Button(LAST_POS(player)).wait_for_press(20):
        return 1
    else:
        return 0

def PLAYER_COLOR(player):
    switcher = {
        0:"Red",
        1:"Yellow",
        2:"Blue",
        3:"Green"
    }
    return switcher[player]

def start():
    START_CHECK()
    global total_players, i
    while len(neighbours) < 12:
        for i in range(total_players):
            if (len(neighbours) >= 12):
                break
            try:
                place_to_go = DICE_1()
                print("{} Go to {}".format(PLAYER_COLOR(i),jacks_repr[place_to_go]))
                time.sleep(0.4)
                if Button(place_to_go).wait_for_press(20):
                    time.sleep(0.4)
                    if BUY(i, place_to_go) != -1:
                        neighbours.append(place_to_go) # so that DICE doesn't give u same pos twice
                        pixels[jacks_diodes[place_to_go]] = colors[PLAYER_COLOR(i)]
                        pixels.show()
                    else:
                        pixels[jacks_diodes[place_to_go]] = colors["Wrong"]
                        pixels.show()
                        while not GO_BACK(i):
                            GO_BACK(i)
                        pixels[jacks_diodes[place_to_go]] = colors["Black"]
                        pixels.show()

                else:
                    print("Error else - start anew")
                    exit(1)
            except TypeError as e:
                print(p1)
                print(p2)
                print(p3)
                print(p4)
                print ("ERROR: {}".format(e))
                continue
# End of Functions for beggining
def CURR_STATE():
    print('''This is the current state:\n\
    Red    - on {:3} with {}$ and {} lives\n\
    Yellow - on {:3} with {}$ and {} lives\n\
    Blue  - on {:3} with {}$ and {} lives\n\
    Green  - on {:3} with {}$ and {} lives'''.format(\
    jacks_repr[p1.curr_position], p1.money, p1.lives,\
    jacks_repr[p2.curr_position], p2.money, p2.lives,\
    jacks_repr[p3.curr_position], p3.money, p3.lives,
    jacks_repr[p4.curr_position], p4.money, p4.lives))
# Start of Functions for main program
def DICE_2(i):

    move_to = jacks_pins.index(LAST_POS(i)) + random.choice([1, 2, 3, 4, 5, 6])
    if move_to >= 12:
        move_to -= 12
    if Button(jacks_pins[move_to]).is_pressed:
        return DICE_2(i)
    return move_to

def ENEMY(player, pos):
    # if position in players arsenal - returns (-1) else returns the owner of the position
    switch = {
        0:p1.owned_pos,
        1:p2.owned_pos,
        2:p3.owned_pos,
        3:p4.owned_pos
    }

    if pos in switch[player]:
        return -1
    else:
        if pos in p1.owned_pos:
            return 0
        elif pos in p2.owned_pos:
            return 1
        elif pos in p3.owned_pos:
            return 2
        elif pos in p4.owned_pos:
            return 3

def TAKE_HP(player):
    pass

def ASK(form, to):
    pass
    # print("{} ask {} a question".format(PLAYER_COLOR(0), PLAYER_COLOR(1))
    # while 1:
    #     if Button(26).is_pressed:
    #         TAKE_HP(to)
    #     elif Button(17).is_pressed:
    #         break

def MAIN():
    global i
    while True:
        i += 1
        if i == 4:
            i = 0
        dice_res = DICE_2(i) # 100% there isn't another player - comes form DICE Function
        print("{} go To {}".format(PLAYER_COLOR(i), jacks_repr[move_to]))
        if Button(move_to).wait_for_press(20):
            enemy = ENEMY(i, move_to)
            if enemy == -1:
                continue
            else:
                QUESTION(enemy, i)



if __name__ == "__main__":
    LED_START()
    print("Press the Black Button to start the game")
    Button(2).wait_for_press()
    print("started")
    start()

    print(p1)
    print(p2)
    print(p3)
    print(p4)
    # CURR_STATE()
    MAIN()
