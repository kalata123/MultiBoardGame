import gpiozero
import time
from Classes import *
import random

jacks_repr = {
    13:"I",
    # 7:"II", # на късо свързано и винаги е pushed state - hardware error
    6:"III",
    8:"IV",
    3:"V",
    1:"VI",
    20:"VII",
    27:"VIII",
    19:"IX",
    24:"X",
    23:"XI",
    25:"XII",
    16:"XIII",
    # 21:"XIV", # на късо свързано и винаги е pushed state - hardware error
    12:"XV",
    5:"XVI",
    26:"BLB",
    2:"BB",
    17:"RB"

}

jacks_pins = [
    13,
    # 7, # на късо свързано и винаги е pushed state - hardware error
    6,
    8,
    3,
    1,
    20,
    27,
    19,
    24,
    23,
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

def START_CHECK():
    # checks if the board is clear from palms
    j = 0
    while j is not 14:
        j = 0
        print("i=0")
        for i in jacks_pins:
            try:
                if gpiozero.Button(i).is_pressed:
                    if gpiozero.Button(i).is_held:
                        print("it is held")
                    print("Take out {} palm".format(jacks_repr[i]))
                    break
                else:
                    print(" i = {}".format(i))
                    j += 1
            except RuntimeError as e:
                print(e)

def DICE_1():
    a = random.choice(jacks_pins)
    if a in neighbours:
        return DICE_1()
    else:
        return a

def pl1(pos, lives=3, money=300):
    global p1

    p1 = Player(lives, money, pos)
    if pos not in p1.owned_pos:
        p1.owned_pos.append(pos)
        print("adding {}".format(p1.owned_pos))
    return p1
def pl2(pos, lives=3, money=300):
    global p2
    p2 = Player(lives, money, pos)
    p2.owned_pos.append(pos)
    return p2
def pl3(pos, lives=3, money=300):
    global p3
    p3 = Player(lives, money, pos)
    p3.owned_pos.append(pos)
    return p3
def pl4(pos, lives=3, money=300):
    global p4
    p4 = Player(lives, money, pos)
    p4.owned_pos.append(pos)
    return p4
def INIT_PL(player, pos):
    # initialises a player
    switcher = {
        1:pl1(pos),
        2:pl2(pos),
        3:pl3(pos),
        4:pl4(pos)
    }


# START_CHECK()

place_to_go = DICE_1()
print("Go to {}".format(place_to_go))
gpiozero.Button(place_to_go).wait_for_press()
INIT_PL(1, place_to_go)
print("printit {} {}".format(p1, p1.owned_pos))
for i in p1.owned_pos:
    print(i)





# neighbours = []
#
# jacks_pins = [
#     13,
#     # 7, # на късо свързано и винаги е pushed state - hardware error
#     6,
#     8,
#     3,
#     1,
#     20,
#     27,
#     19,
#     24,
#     23,
#     25,
#     16,
#     # 21, # на късо свързано и винаги е pushed state - hardware error
#     12,
#     5
# ]
#
# buttons_pins = [
#     26,
#     2,
#     17
# ]
#
# bad_jacks = [
#     6,
#     8,
#     1,
#     20,
#     24,
#     25,
#     12,
#     5
# ]
#
# b = Classes.Board(jacks_pins, buttons_pins, neighbours)
# p1 = Classes.Player(3, 200)
# p2 = Classes.Player(3, 200)
# p3 = Classes.Player(3, 200)
# p4 = Classes.Player(3, 200)
#
# def CHECK_NEIGH():
#     # checks the board jacks,
#     # and if all in are in neighbour table does nothing
#     # else adds it.
#
#     for i in jacks_pins:
#         if gpiozero.Button(i).is_pressed:
#             b.ADD_NEIGHBOUR(i)
#         else:
#             b.REMOVE_NEIGHBOUR(i)
# def SET_PL_to_POS(neigh_table):
#     p1.NEW_POSITION(neigh_table[0])
#     p2.NEW_POSITION(neigh_table[1])
#     p3.NEW_POSITION(neigh_table[2])
#     p4.NEW_POSITION(neigh_table[3])
# def DICE():
#     print("The dice has been diced")
#     a = random.choice(jacks_pins)
#     if a in neighbours:
#         DICE()
#     else:
#         print("move to {}".format(a))
#         return a
#
# CHECK_NEIGH()
# # SET_PL_to_POS(neighbours)
# while True:
#     if gpiozero.Button(2).is_pressed:
#         a = DICE()
#         print("Butt was pressed and dice is {}".format(a))
#         gpiozero.Button(a).wait_for_press()
#         p1.NEW_POSITION(a)
#     if p1.position in bad_jacks:
#         print("this is gonna be bad")
#     else:
#         print("You are safe")
#     # print(p1)
#     # print(p2)
#     # print(p3)
#     # print(p4)
#     # print(neighbours)
#     #print("none for now")
