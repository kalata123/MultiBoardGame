import gpiozero
import time
from Classes import Player
import random


p1 = Player("Red",3,600,0)
p2 = Player("Yellow",3,600,1)
p3 = Player("White",3,600,2)
p4 = Player("Black",3,600,3)
total_players = 4

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
    17:"Black Button",
    2:"Blue Button",
    26:"Red Button"

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
# Functions for beggining
def START_CHECK():
    # checks if the board is clear from palms
    j = 0
    while j is not len(jacks_repr.keys()) - 3:
        j = 0
        for i in jacks_pins:
            try:
                if gpiozero.Button(i).is_pressed:
                    print("Take out {} palm".format(jacks_repr[i]))
                    gpiozero.Button(i).wait_for_release()
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
    print("You don't have enough money to buy this position\nPlease go back to {}"\
    .format(jacks_repr[LAST_POS(player)]))
    if gpiozero.Button(LAST_POS(player)).wait_for_press(20):
        return 1
    else:
        return 0

def PLAYER_COLOR(player):
    switcher = {
        0:"Red",
        1:"Yellow",
        2:"White",
        3:"Black"
    }
    return switcher[player]

def start():
    START_CHECK()
    global total_players
    while len(neighbours) < 12:
        for i in range(total_players):
            if (len(neighbours) >= 12):
                break
            try:
                place_to_go = DICE_1()
                print("{} Go to {}".format(PLAYER_COLOR(i),jacks_repr[place_to_go]))
                time.sleep(0.4)
                if gpiozero.Button(place_to_go).wait_for_press(20):
                    time.sleep(0.4)
                    if BUY(i, place_to_go) != -1:
                        neighbours.append(place_to_go) # so that DICE doesn't give u same pos twice
                    else:
                        while not GO_BACK(i):
                            GO_BACK(i)

                else:
                    print("Error else - start anew")
                    exit(1)
            except TypeError as e:
                print(p1)
                print(p2)
                print(p3)
                print(p4)
                print(e)
                continue
# End of Functions for beggining
def CURR_STATE():
    print('''This is the current state:\n\
    Red    - on {:3} with {}$ and {} lives\n\
    Yellow - on {:3} with {}$ and {} lives\n\
    White  - on {:3} with {}$ and {} lives\n\
    Black  - on {:3} with {}$ and {} lives'''.format(\
    jacks_repr[p1.curr_position], p1.money, p1.lives,\
    jacks_repr[p2.curr_position], p2.money, p2.lives,\
    jacks_repr[p3.curr_position], p3.money, p3.lives,
    jacks_repr[p4.curr_position], p4.money, p4.lives))
# Start of Functions for main program
def DICE_2():
    return random.choice([1, 2, 3, 4, 5, 6])

def MAIN():
    pass

if __name__ == "__main__":
    gpiozero.Button(2).wait_for_press()
    start()
    CURR_STATE()
    MAIN()
