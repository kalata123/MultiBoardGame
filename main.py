from board import D18
from neopixel import NeoPixel
from gpiozero import Button
from time import sleep
from random import choice, randint
from Classes import Player
from os import system
from json import load

colors = {
'Game' : (50,40,30),
'Black': (0,0,0),
'Wrong' : (50,255,255),
'Goto' : (0,255,255),
'Start' : (200,200,200)
}

led_count = 16
pixels = NeoPixel(D18, led_count, auto_write=True)

def setup():
    global total_players, player_names, comp_pos, led_count, pixels, i, colors, p1, p2, p3, p4, switch, neigh_in_use
    total_players = 0
    player_names = []
    comp_pos = []
    neigh_in_use = [] # used in dices in order not to cause threading errors :)


    i = 0
    pname = ''
    while total_players < 2 or total_players > 4:
        total_players = int(input("How many are playing? - "))

    stlives = 0
    while stlives < 3:
        stlives = int(input('How many lives do you want to have? - '))

    stmoney = 0
    while stmoney < 100:
        stmoney = int(input('How much money do yo want to have? - '))

    for _ in range(total_players):
        sleep(0.3)
        pixels.fill(colors['Game'])
        sleep(0.3)
        pixels.fill(colors['Wrong'])

    for _ in range(total_players):
        neigh_in_use.append(0)
        pname = str(input("Give me your names :)"))
        while player_names.count(pname) >= 1:
            print("try again")
            pname = str(input("Give me your names :)"))
        else:
            player_names.append(pname)

    p0 = Player('Game', 10000000, 9999999999999, -1)
    p1 = Player(player_names[0], stlives, stmoney, 0)
    p2 = Player(player_names[1], stlives, stmoney, 1)
    switch = {
    'The game': p0,
    0:p1,
    1:p2
    }

    colors[switch[0].name] = (255,250,0)
    colors[switch[1].name] = (0,0,255)

    if total_players >= 3:
        p3 = Player(player_names[2], stlives, stmoney, 2)
        colors[player_names[2]] = (0,255,0)
        switch[2] = p3
    if total_players > 3:
        p4 = Player(player_names[3], stlives, stmoney, 3)
        colors[player_names[3]] = (255,0,0)
        switch[3] = p4

jacks_diodes = {
    12:15,
    9:14,
    13:13,
    22:12,
    6:11,
    8:10,
    3:9,
    10:8,
    20:7,
    27:6,
    19:5,
    24:4,
    23:3,
    25:2,
    16:1,
    21:0
}

jacks_repr = {
    13:"I",
    # 22:"II",
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

jacks_pins = [
    13,
    # 22,
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

buttons_pins = {
    'Black' : 26,
    'Middle' : 2,
    'Red' : 17
}

neighbours = []
# LED Functions
def COLORISE():
    global pixels, switch, colors
    comp = False
    pixels.fill(colors["Black"])
    for i in range(0,len(jacks_pins)):
        for l in range(total_players):
            if jacks_pins[i] in switch[l].owned_pos:
                pixels[jacks_diodes[jacks_pins[i]]] = colors[switch[l].name]
            elif jacks_pins[i] in comp_pos:
                pixels[jacks_diodes[jacks_pins[i]]] = colors['Game']

def LED_START(with_revercing=False, end='Start'):
    global pixels
    for _ in range(5):
        for i in range(len(jacks_pins)):
            pixels[jacks_diodes[jacks_pins[i]]] = choice(list(colors.values()))

            sleep(0.01)
    if with_revercing:
        COLORISE()
    else:
        pixels.fill(colors[end])

# Functions for beggining
def START_CHECK():
    # checks if the board is clear from palms
    global pixels, jacks_pins, jacks_diodes, colors
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

def CONDITION(player, all=False):
    global total_players, switch
    if not all:
        return switch[player].condition
    else:
        for i in range(total_players):
            if switch[i].condition: # there is still a player with money
                return -1
        return 0 #all players are poor

def FATTEMPTS(player):
    global switch
    return switch[player].failed_attempts

def BUY(player, pos, money_to_pay = 100):
    # gives <pos> over to <player> and
    # changes <player>'s curr_position
    # DO NOT try to improve with switch dictionary - already tried
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
    global total_players, switch, jacks_repr
    print('''This is the current state:\n\
    {:10} - on {:3} with {}$ and {} lives\n\
    {:10} - on {:3} with {}$ and {} lives\n\
    '''.format(\
        switch[0].name, jacks_repr[switch[0].curr_position], switch[0].money, switch[0].lives,\
        switch[1].name, jacks_repr[switch[1].curr_position], switch[1].money, switch[1].lives))
    if total_players >= 3:
        print("{:10} - on {:3} with {}$ and {} lives".format(switch[2].name,\
        jacks_repr[switch[2].curr_position], switch[2].money, switch[2].lives))
    if total_players > 3:
        print("{:10} - on {:3} with {}$ and {} lives".format(switch[3].name,\
        jacks_repr[switch[3].curr_position], switch[3].money, switch[3].lives))

def START():
    print("goes in start()")
    START_CHECK()
    global total_players, i, comp_pos, neigh_in_use, pixels
    global neighbours, jacks_pins, switch, colors, jacks_diodes, jacks_repr
    while len(neighbours) < len(jacks_pins):
        for i in range(total_players):
            if (len(neighbours) >= len(jacks_pins)):
                break
            try:
                place_to_go = DICE_1()
                if CONDITION(i) == True and FATTEMPTS(i) < 1:
                    print(CONDITION(i))
                    print(FATTEMPTS(i))
                    system("clear")
                    print("{} Go to {}".format(PLAYER_COLOR(i), jacks_repr[place_to_go]))
                    pixels[jacks_diodes[place_to_go]] = colors["Goto"]
                    sleep(0.4)
                    if Button(place_to_go).wait_for_press(20): # Sometimes gives SegmentationFault Exactly here
                        sleep(0.4)
                        print("to buy")
                        if BUY(i, place_to_go) != -1:
                            print("Buying")
                            neigh_in_use[i] = switch[i].curr_position
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
    global neigh_in_use
    move_to = neigh_in_use[0]
    rand = choice([1, 2, 3, 4, 5, 6])
    while move_to in neigh_in_use:
        try:
            move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand]
        except IndexError as e:
            move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand - len(jacks_pins)]

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
    questions = load(open("/home/pi/Desktop/TUESFest2019/Comp_questions.json", "r"))
    return list(questions.values())[randint(0,len(questions.values())-1)]

def PLAY_AGAIN():
    print("This game is over, would you like to play again? (Hit Black Button for Yes and Red for No)")
    while  1:
        if Button(buttons_pins['Black']).is_pressed:
            GAME()
            break
        elif Button(buttons_pins['Red']).is_pressed:
            exit(1)
            break
        else:
            continue

def WINNER(player):
    global switch
    CURR_STATE()
    print("Congrats {} you jsut won the game".format(switch[player].name))
    LED_START(end = switch[player].name)
    PLAY_AGAIN()

def CHECK_ALL():
    global switch, total_players
    j = 0
    i = 0
    for i in range(total_players):
        if switch[i].lives > 0:
            j += 1
    if j < 2:
        WINNER(i)

def CHECK_P_STATUS(doer, taker):
    global switch
    if switch[taker].lives <=0:
        switch[doer].owned_pos.append(switch[taker].owned_pos)
        COLORISE()
        CHECK_ALL()

def TAKE(what_to_take, doer, taker, money=50, lives=1):
    global switch

    if what_to_take.lower() == 'hp':
        switch[taker].lives -= lives
        switch[doer].lives += lives
        CHECK_P_STATUS(doer, taker)

    elif what_to_take.lower() == 'money':
        switch[taker].money -= money
        switch[doer].money += money
        if switch[taker].money <=0:
            print("Sorry you don't have enough money to pay the tax -> One of your lives will be taken")
            TAKE('hp', doer, taker)

def SENTENCE(to, frm='The game'):
    system("clear")
    if frm != 'The game':
        print("{tfrm} hit Black Button to let {tto} go for free\n\
Hit Middle Button to take {tto} 50$\n\
Hit Red Button to take {tto} 1 HP".format(tfrm=PLAYER_COLOR(frm), tto = PLAYER_COLOR(to)))
    else:
        print('{tfrm} asked a question and {tto} has to answer it,\n\
Hit Middle Button to take {tto} 50$\n\
Hit Red Button to take {tto} 1 HP^)'.format(tfrm=PLAYER_COLOR(frm), tto = PLAYER_COLOR(to)))
    try:
        while True:
            if Button(buttons_pins['Middle']).is_pressed: # Take money
                print('Taking Money')
                TAKE('money', frm, to)
                sleep(0.3)
                break
            elif Button(buttons_pins['Red']).is_pressed: # Take HP
                print('Taking HP')
                TAKE('HP', frm, to)
                sleep(0.3)
                break
            elif Button(buttons_pins['Black']).is_pressed: # Free to go
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
    if frm == -2:
        MQUESTION()
        SENTENCE(to)
    else:
        print('{} to ask {} a guestion hit the Black Button\n\
after he has answered you have to decide\n\
whether to take nothing, money or HP from him\n\n\
Of course you can choose to let me ask a question - \
just hit the Middle button'.format(PLAYER_COLOR(frm), PLAYER_COLOR(to)))
        while 1:
            if Button(buttons_pins['Middle']).is_pressed: # MQuestion
                sleep(0.1)
                print(MQUESTION())
                SENTENCE(to,frm)
                break

            elif Button(buttons_pins['Black']).is_pressed: # I'll ask myself
                sleep(0.1)
                SENTENCE(to, frm)

            else: # Continue
                continue
            break

def MAIN():
    global switch, neigh_in_use, colors, i, pixels # its global cos i is currently the player in order to move
    while True:
        dice_res = DICE_2(i) # 100% there isn't another player - comes form DICE Function
        i += 1
        if i >= total_players:
            i = 0
        system("clear")
        print("{} go To {}".format(PLAYER_COLOR(i), jacks_repr[dice_res]))
        pixels[jacks_diodes[dice_res]] = colors['Goto']

        if Button(dice_res).wait_for_press():
            neigh_in_use[i] = switch[i].curr_position
            enemy = ENEMY(i, dice_res)
            if enemy == -1: # its my field, not enemie's
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(i)]
                continue
            elif enemy == -2: # has to be went on
                print("The comp will ask")
                ASK(enemy, i)
                pixels[jacks_diodes[dice_res]] = colors['Game']
            else: # enemy field
                print("ASK")
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(enemy)]
                ASK(enemy, i)

def GAME():
    LED_START(end='Wrong')
    setup()
    LED_START(end='Game')
    print("Press the Middle Button to start the game")
    Button(buttons_pins['Middle']).wait_for_press()
    LED_START()
    print("Now the second part begins")
    START()
    CURR_STATE()
    LED_START(True)
    sleep(1)
    MAIN()

if __name__ == "__main__":
    # GAME()
    PLAY_AGAIN()
