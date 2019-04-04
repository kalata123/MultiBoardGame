from board import D18
from neopixel import NeoPixel
from gpiozero import Button
from time import sleep
from random import choice
from Classes import Player
from os import system



def goforit():
    global total_players, player_names, comp_pos, led_count, pixels, i, colors, p1, p2, p3, p4, switch
    total_players = 0
    player_names = []
    comp_pos = []


    led_count = 16
    pixels = NeoPixel(D18, led_count, auto_write=True)

    i = 0
    pname = ''
    while total_players < 2 or total_players > 4:
        total_players = int(input("How many are playing? - "))
    for i in range(total_players):
        pname = str(input("Give me your names :)"))
        while player_names.count(pname) >= 1:
            print("try again")
            pname = str(input("Give me your names :)"))
        else:
            player_names.append(pname)

    colors = {
        player_names[0] : (255,250,0),
        player_names[1] : (0,0,255),
        'Game' : (50,40,30),
        'Black': (0,0,0),
        'Wrong' : (50,255,255),
        'Goto' : (0,255,255),
        'Start' : (200,200,200)
        }

    p1 = Player(player_names[0], 3, 100, 0)
    p2 = Player(player_names[1], 3, 100, 1)
    switch = {
    0:p1,
    1:p2
    }
    if total_players >= 3:
        p3 = Player(player_names[2], 3, 600, 2)
        colors[player_names[2]] = (0,255,0)
        switch[2] = p3
    if total_players == 4:
        p4 = Player(player_names[3], 3, 600, 3)
        colors[player_names[3]] = (255,0,0)
        switch[2] = p3


jacks_diodes = {
    12:15,
    5:14,
    13:13,
    # 7:12,
    6:11,
    8:10,
    3:9,
    # 1:8,
    20:7,
    27:6,
    19:5,
    24:4,
    # 23:3,
    25:2,
    16:1,
    21:0
}

jacks_repr = {
    13:"I",
    # 7:"II", #
    6:"III",
    8:"IV",
    3:"V",
    # 1:"VI", #
    20:"VII",
    27:"VIII",
    19:"IX",
    24:"X",
    # 23:"XI",
    25:"XII",
    16:"XIII",
    # 21:"XIV", #
    12:"XV",
    5:"XVI",
    # Buttons
    26:"Black Button",
    2:"Middle Button",
    17:"Red Button"

}

jacks_pins = [
    13,
    # 7, # from the Raspberry Pi Zero W - always is_pressed
    6,
    8,
    3,
    # 1, # Could be from the Raspberry Pi Zero W - never is_pressed
    20,
    27,
    19,
    24,
    # 23, # Could be from the Raspberry Pi Zero W - never is_pressed
    25,
    16,
    # 21, # from the Raspberry Pi Zero W - always is_pressed
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
    global pixels
    for _ in range(5):
        for i in range(len(jacks_pins)):
            pixels[jacks_diodes[jacks_pins[i]]] = choice(list(colors.values()))

            sleep(0.01)
    pixels.fill(colors["Start"])

# Functions for beggining
def START_CHECK():
    # checks if the board is clear from palms
    j = 0
    while j is not len(jacks_pins):
        j = 0
        for i in jacks_pins:
            try:
                if Button(i).is_pressed:
                    system("clear")
                    print("Take out {} palm".format(jacks_repr[i]))
                    pixels[jacks_diodes[i]] = colors['Wrong']

                    Button(i).wait_for_release()
                    pixels[jacks_diodes[i]] = colors['Start']

                j += 1
            except RuntimeError as e:
                print(e)

def DICE_1():
    # returns a random pin number from jacks_pins list
    a = choice(jacks_pins)
    if a not in neighbours:
        return a
    return DICE_1()

def CONDITION(player,all=False):
    global total_players, switch
    if not all:
        return switch[player].condition
    else:
        for i in range(total_players):
            if switch[i].condition: # there is still a player with money
                return -1
        return 0 #all players are poor


def FATTEMPTS(player):
    global total_players
    switch = {
        0:p1.failed_attempts,
        1:p2.failed_attempts,
    }
    if total_players >= 3:
        switch[2] = p3.failed_attempts
    if total_players > 3:
        switch[3] = p4.failed_attempts
    return switch[player]

def BUY(player, pos, money_to_pay = 100):
    # gives <pos> over to <player> and
    # changes <player>'s curr_position
    if player == 0:
        return p1.ADD_POSITION(pos, money_to_pay)
    elif player == 1:
        return p2.ADD_POSITION(pos, money_to_pay)
    elif player == 2:
        return p3.ADD_POSITION(pos, money_to_pay)
    elif player == 3:
        return p4.ADD_POSITION(pos, money_to_pay)

def LAST_POS(player):
    global switch
    # switch = {
    #     0:p1.curr_position,
    #     1:p2.curr_position
    # }
    #
    # global total_players
    # if total_players >= 3:
    #     switch[2]=p3.curr_position
    # if total_players > 3:
    #     switch[3]=p4.curr_position
    return switch[player].curr_position

def GO_BACK(player):
    system("clear")
    print("You don't have enough money to buy this position\nPlease go back to {} - You have 20 seconds"\
    .format(jacks_repr[LAST_POS(player)]))
    if Button(LAST_POS(player)).wait_for_press(20):
        return 1
    else:
        return 0

def PLAYER_COLOR(player):
    global switch
    return switch[player].name

def CURR_STATE():
    # Should be optimized when there are 2 players to show only their parameters
    global total_players
    print('''This is the current state:\n\
    {:10} - on {:3} with {}$ and {} lives\n\
    {:10} - on {:3} with {}$ and {} lives\n\
    '''.format(\
        player_names[0], jacks_repr[p1.curr_position], p1.money, p1.lives,\
        player_names[1], jacks_repr[p2.curr_position], p2.money, p2.lives))
    if total_players >= 3:
        print("{:10} - on {:3} with {}$ and {} lives".format(player_names[2],\
        jacks_repr[p3.curr_position], p3.money, p3.lives))
    if total_players > 3:
        print("{:10} - on {:3} with {}$ and {} lives".format(player_names[3],\
        jacks_repr[p4.curr_position], p4.money, p4.lives))


def START():
    print("goes in start()")
    START_CHECK()
    global total_players, i, comp_pos
    while len(neighbours) < len(jacks_pins):
        for i in range(total_players):
            if (len(neighbours) >= 12):
                break
            try:
                place_to_go = DICE_1()
                if CONDITION(i) == True and FATTEMPTS(i) < 1:
                    print("in for - {}".format(i))
                    print(CONDITION(i))
                    print(FATTEMPTS(i))
                    system("clear")
                    print("{} Go to {}".format(PLAYER_COLOR(i),jacks_repr[place_to_go]))
                    pixels[jacks_diodes[place_to_go]] = colors["Goto"]

                    sleep(0.4)
                    if Button(place_to_go).wait_for_press(20):
                        sleep(0.4)
                        if BUY(i, place_to_go) != -1:
                            print("Buying")
                            neighbours.append(place_to_go) # so that DICE doesn't give u same pos twice
                            pixels[jacks_diodes[place_to_go]] = colors[PLAYER_COLOR(i)]

                        else:
                            pixels[jacks_diodes[place_to_go]] = colors["Wrong"]

                            while not GO_BACK(i):
                                GO_BACK(i)
                            pixels[jacks_diodes[place_to_go]] = colors["Start"]


                    else:
                        print("Error else - start anew")
                        system("clear")
                        exit(1)

                elif CONDITION(i,True) == 0:
                    print("Now all places belong to the game")
                    neighbours.append(place_to_go)
                    comp_pos.append(place_to_go)
                    pixels[jacks_diodes[place_to_go]] = colors['Game']

                else:
                    # if both are with 0 money  its while True
                    continue
            except TypeError as e:
                CURR_STATE()
                print ("ERROR: {}".format(e))
                continue
# End of Functions for beggining


# Start of Functions for main program
def DICE_2(player):
    # returns a number between 1 and 6,
    # warrant - the position it is pointing to not be a is_pressed jack
    rand = choice([1, 2, 3, 4, 5, 6])
    try:
        move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand]
    except IndexError as e:
        move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand - len(jacks_pins)]

    if Button(move_to).is_pressed:
        return DICE_2(player)
    return move_to

def ENEMY(player, pos):
    # if position in players arsenal - returns (-1) else returns the owner of the position
    global total_players, switch, comp_pos
    if pos in switch[player].owned_pos:
        return -1
    else:
        for i in range(total_players):
            if pos in switch[i].owned_pos:
                return i
            if pos in comp_pos:
                return -2

def MQUESTION():
    return choice(['question ONE','question 2','question 3','question 4'])

def TAKE(what_to_take, doer, taker, money=50, lives=1):
    global p1, p2, p3, p4, switch

    if what_to_take.lower() == 'hp':
        switch[taker].lives -= lives
        switch[doer].lives += lives
    elif what_to_take.lower() == 'money':
        switch[taker].money -= money
        switch[doer].money += money

def SENTENCE(frm, to):
    system("clear")
    print("{} hit Black Button to let {} go for free\n\
Hit Middle Button to take {} 50$\n\
Hit Red Button to take {} 1 HP".format(PLAYER_COLOR(frm, to, to, to)))
    try:
        while True:
            if Button(2).is_pressed: # Take money
                print('Taking Money')
                TAKE('money', frm, to)
                sleep(0.3)
                break
            elif Button(17).is_pressed: # Take HP
                print('Taking HP')
                TAKE('HP', frm, to)
                sleep(0.3)
                break
            elif Button(26).is_pressed: # Free to go
                print('Free to Go')
                sleep(0.3)
                break
            else:
                sleep(0.01)
                continue

    except RuntimeError as e:
        print('RuntimeErroR: {}'.format(e))

def ASK(frm, to):
    system("clear")
    print('{} to ask {} a guestion hit the Black Button\n\
after he has answered you have to decide\n\
whether to take nothing, money or HP from him\n\n\
Of course you can choose to let me ask a question - \
just hit the Middle button'.format(PLAYER_COLOR(frm), PLAYER_COLOR(to)))
    while 1:
        if Button(2).is_pressed: # MQuestion
            print(MQUESTION())
            SENTENCE(frm, to)
            break

        elif Button(26).is_pressed: # I'll ask myself
            SENTENCE(frm, to)

        else: # Continue
            continue

        break

def MAIN():
    global i # its global cos i is currently the player in order to move
    while True:
        dice_res = DICE_2(i) # 100% there isn't another player - comes form DICE Function
        i += 1
        if i >= total_players:
            i = 0
        system("clear")
        print("{} go To {}".format(PLAYER_COLOR(i), jacks_repr[dice_res]))
        pixels[jacks_diodes[dice_res]] = colors['Goto']

        if Button(dice_res).wait_for_press():
            enemy = ENEMY(i, dice_res)
            if enemy == -1: # its my field, not enemie's
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(i)]

                continue
            elif enemy == -2: # has to be went on
                print("The comp will ask")
                pixels[jacks_diodes[dice_res]] = colors['Game']
            else: # enemy field
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(enemy)]
                ASK(enemy, i)

if __name__ == "__main__":
    goforit()
    LED_START()
    print("Press the Middle Button to start the game")
    Button(2).wait_for_press()
    print("started")
    START()
    CURR_STATE()
    MAIN()
