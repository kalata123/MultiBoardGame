from gpiozero import Button
import time
from Classes import Player
import random
import board
from neopixel import NeoPixel

led_count = 16
i = 0

pixels = NeoPixel(board.D18, led_count, auto_write=False)

# initialising the players - should be made - dynamic - if 2 players => 2 players, not 4
total_players = 4
p1 = Player("Red", 3, 600, 0)
p2 = Player("Yellow", 3, 600, 1)
p3 = Player("Blue", 3, 600, 2)
p4 = Player("Green", 3, 600, 3)

colors = {
    "Yellow" : (255,250,0),
    'Blue' : (0,0,255),
    "Red" : (0,255,0),
    'Green' : (255,0,0),
    'Black': (0,0,0),
    'Wrong' : (50,255,255),
    'Goto' : (0,255,255),
    'Start' : (200,200,200)
    }

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
    2:"Black Button",
    26:"Blue Button",
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
            pixels[jacks_diodes[jacks_pins[i]]] = random.choice(list(colors.values()))
            pixels.show()
            time.sleep(0.01)
    pixels.fill(colors["Start"])
    pixels.show()
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
                    pixels[jacks_diodes[i]] = colors['Red']
                    pixels.show()
                    Button(i).wait_for_release()
                    pixels[jacks_diodes[i]] = colors['Start']
                    pixels.show()
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
    print("You don't have enough money to buy this position\nPlease go back to {} - You have 20 seconds"\
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
    return switcher.get(player,"Not in Dict")

def START():
    START_CHECK()
    global total_players, i
    while len(neighbours) < 12:
        for i in range(total_players):
            if (len(neighbours) >= 12):
                break
            try:
                place_to_go = DICE_1()
                print("{} Go to {}".format(PLAYER_COLOR(i),jacks_repr[place_to_go]))
                pixels[jacks_diodes[place_to_go]] = colors["Goto"]
                pixels.show()
                time.sleep(0.4)
                if Button(place_to_go).wait_for_press(20):
                    time.sleep(0.4)
                    if BUY(i, place_to_go) != -1:
                        print('buy != -1')
                        neighbours.append(place_to_go) # so that DICE doesn't give u same pos twice
                        pixels[jacks_diodes[place_to_go]] = colors[PLAYER_COLOR(i)]
                        pixels.show()
                    else:
                        print('buy = else ')
                        pixels[jacks_diodes[place_to_go]] = colors["Wrong"]
                        pixels.show()
                        while not GO_BACK(i):
                            GO_BACK(i)
                        pixels[jacks_diodes[place_to_go]] = colors["Start"]
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
    # Should be optimized when there are 2 players to show only their parameters
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
def DICE_2(player):
    # returns a number between 1 and 6,
    # warrant - the position it is pointing to not be a is_pressed jack
    rand = random.choice([1, 2, 3, 4, 5, 6])
    try:
        move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand]
    except IndexError as e:
        print(LAST_POS(player))
        print(rand)
        print(len(jacks_pins))
        move_to = jacks_pins[jacks_pins.index(LAST_POS(player)) + rand - len(jacks_pins)]

    if Button(move_to).is_pressed:
        return DICE_2(player)
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

def MQUESTION():
    return random.choice(['question ONE','question 2','question 3','question 4'])

def TAKE(what_to_take, doer, taker, money=50, lives=1):
    global p1, p2, p3, p4
    switch = {
        0:p1,
        1:p2,
        2:p3,
        3:p4
    }
    if what_to_take.lower() == 'hp':
        switch[taker].lives -= lives
        switch[doer].lives += lives
    elif what_to_take.lower() == 'money':
        switch[taker].money -= money
        switch[doer].money += money

def SENTENCE(frm, to):
    print("{} hit Black Button to let go for free\n\
Hit Middle Button to take 50$ money\n\
Hit Red Button to 1 take HP".format(frm))
    try:
        while True:
            if Button(2).is_pressed: # Take money
                print('Taking Money')
                TAKE('money', frm, to)
                time.sleep(0.3)
                break
            elif Button(17).is_pressed: # Take HP
                print('Taking HP')
                TAKE('HP', frm, to)
                time.sleep(0.3)
                break
            elif Button(26).is_pressed: # Free to go
                print('Free to Go')
                time.sleep(0.3)
                break
            time.sleep(0.01)
    except RuntimeError as e:
        print('RuntimeErroR: {}'.format(e))
    except RuntimeError as e:
        print('RuntimeErroR: {}'.format(e))
    except RuntimeError as e:
        print('RuntimeErroR: {}'.format(e)) 

def ASK(frm, to):
    print('{} to ask {} a guestion hit the Black Button\n\
after he has answered you have to decide\n\
whether to take nothing, money or HP from him\n\
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
        i += (1 if i <=3 else 0)
        if i >= 4:
            i = 0
        dice_res = DICE_2(i) # 100% there isn't another player - comes form DICE Function
        print("{} go To {}".format(PLAYER_COLOR(i), jacks_repr[dice_res]))
        pixels[jacks_diodes[dice_res]] = colors['Goto']
        pixels.show()
        if Button(dice_res).wait_for_press():
            enemy = ENEMY(i, dice_res)
            if enemy == -1: # its my field, not enemie's
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(i)]
                pixels.show()
                continue
            else: # enemy field
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(enemy)]
                pixels.show()
                ASK(enemy, i)

if __name__ == "__main__":
    LED_START()
    print("Press the Middle Button to start the game")
    Button(2).wait_for_press()
    print("started")
    START()
    CURR_STATE()
    MAIN()
