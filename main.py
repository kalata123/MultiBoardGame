# WOrking with 2 players, tried
# notw orking properly with 4 players, tried

from board import D18
from neopixel import NeoPixel
from gpiozero import Button
from time import sleep
from random import choice, randint
from Classes import Player
from os import system
from json import load

colors = {
    'Game': (50, 40, 30),
    'Black': (0, 0, 0),
    'Wrong': (50, 255, 255),
    'Goto': (0, 255, 255),
    'Start': (200, 200, 200)
}

led_count = 16
pixels = NeoPixel(D18, led_count, auto_write=True)


def setup():
    global total_players, player_names, led_count, pixels, i, colors, p1, p2,\
                p3, p4, switch, neigh_in_use
    total_players = 0
    player_names = []
    neigh_in_use = []  # used in dices in order not to cause threading errors

    i = 0
    pname = ''
    while total_players < 2 or total_players > 4:
        total_players = int(input("Колко играча ще играете? - "))

    stlives = 0
    while stlives < 1:
        stlives = int(input('По колко живота ще има всеки? - '))

    stmoney = 0
    while stmoney < 100:
        stmoney = int(input('С каква начална сума ще започнете? - '))

    for _ in range(total_players):
        sleep(0.3)
        pixels.fill(colors['Game'])
        sleep(0.3)
        pixels.fill(colors['Wrong'])

    for _ in range(total_players):
        neigh_in_use.append(0)
        pname = str(input("Как се казвате :)"))
        while player_names.count(pname) >= 1:
            print("try again")
            pname = str(input("Опс, как се казвате :)"))
        else:
            player_names.append(pname)

    p0 = Player('Game', 10000000, 9999999999999, -1)
    p1 = Player(player_names[0], stlives, stmoney, 0)
    p2 = Player(player_names[1], stlives, stmoney, 1)
    switch = {
        'The game': p0,
        0: p1,
        1: p2
    }

    colors[switch[0].name] = (255, 250, 0)
    colors[switch[1].name] = (0, 0, 255)

    if total_players >= 3:
        p3 = Player(player_names[2], stlives, stmoney, 2)
        colors[player_names[2]] = (0, 255, 0)
        switch[2] = p3
    if total_players > 3:
        p4 = Player(player_names[3], stlives, stmoney, 3)
        colors[player_names[3]] = (255, 0, 0)
        switch[3] = p4


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

buttons_pins = {
    'Black': 26,
    'Middle': 2,
    'Red': 17
}

neighbours = []


# LED Functions
def COLORISE():
    # sets the LEDs for who they belong to
    global pixels, switch, colors
    pixels.fill(colors["Black"])
    for i in range(0, len(jacks_pins)):
        for l in range(total_players):
            if jacks_pins[i] in switch[l].owned_pos:
                pixels[jacks_diodes[jacks_pins[i]]] = colors[switch[l].name]
            elif jacks_pins[i] in switch['The game'].owned_pos:
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

                    print("Извадете пионката на поле {}".format(jacks_repr[i]))
                    pixels[jacks_diodes[i]] = colors['Wrong']

                    Button(i).wait_for_release()
                    pixels[jacks_diodes[i]] = colors['Start']

                j += 1
            except RuntimeError as e:
                print(e)


def DICE_1():
    # returns a random pin number from jacks_pins list
    global neighbours
    print("Натиснете черния бутон за да хвърлите дигиталния зар")
    Button(buttons_pins['Black']).wait_for_press()
    a = choice(jacks_pins)

    if a in neighbours:
        return DICE_1()
    else:
        return a


def CONDITION(player, all=False):
    # returns the condition of the player
    global total_players, switch
    if not all:
        return switch[player].condition
    else:
        for i in range(total_players):
            if switch[i].condition:  # there is still a player with money
                return -1
        # all players are poors
        return 0


def FATTEMPTS(player):
    # returns the buy attempts of the player
    global switch
    return switch[player].failed_attempts


def BUY(player, pos, money_to_pay=100):
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
    # returns the player's position, before change
    global switch
    return switch[player].curr_position


def GO_BACK(player):
    # waits for player to go back to its previous position
    print("Нямате достатъчно пари да закупите тази позиция\nМоля върнете се на\
{}".format(jacks_repr[LAST_POS(player)]))
    if Button(LAST_POS(player)).wait_for_press():
        return 1
    else:
        return 0


def PLAYER_COLOR(player):
    # returns the string representation for the color the player
    global switch
    return switch[player].name


def CURR_STATE():
    # prints the current state of the game and players
    global total_players, switch, jacks_repr
    print('''Това е сегашното състояние:\n\
    {} на {:3} позиция с {} лв. и {} живота\n\
    {} на {:3} позиция с {} лв. и {} живота\n\
    '''.format(
        switch[0].name, jacks_repr[
            switch[0].curr_position], switch[0].money, switch[0].lives,
        switch[1].name, jacks_repr[
            switch[1].curr_position], switch[1].money, switch[1].lives))

    if total_players >= 3:
        print("{} на {:3} позиция с {} лв. и {} живота".format(
            switch[2].name, jacks_repr[switch[2].curr_position],
            switch[2].money, switch[2].lives))

    if total_players > 3:
        print("{} на {:3} позиция с {} лв. и {} живота".format(
            switch[3].name, jacks_repr[switch[3].curr_position], 
            switch[3].money, switch[3].lives))


def GIVE_ALL(player):
    global neighbours, switch, jacks_pins, pixels
    for i in range(len(jacks_pins)):
        if jacks_pins[i] not in neighbours:
            neighbours.append(jacks_pins[i])
            switch[player].ADD_POSITION(jacks_pins[i], 100)
            pixels[jacks_diodes[jacks_pins[i]]] = colors['Game']
        else:
            continue


def START():
    START_CHECK()
    global total_players, i, neigh_in_use, pixels
    global neighbours, jacks_pins, switch, colors, jacks_diodes, jacks_repr
    while len(neighbours) < len(jacks_pins):
        for i in range(total_players):
            if (len(neighbours) >= len(jacks_pins)):
                break
            try:
                if CONDITION(i, True) == 0:
                    GIVE_ALL('The game')
                    print("Сега всички останали полета принадлежат на играта")
                elif CONDITION(i) and FATTEMPTS(i) < 1:
                    place_to_go = DICE_1()
                    system("clear")
                    print("{} отиди на {}".format(PLAYER_COLOR(i), jacks_repr[
                        place_to_go]))
                    pixels[jacks_diodes[place_to_go]] = colors["Goto"]
                    sleep(0.4)
                    if Button(place_to_go).wait_for_press():
                        # Sometimes gives SegmentationFault Exactly here
                        sleep(0.4)
                        if BUY(i, place_to_go) != -1:
                            neigh_in_use[i] = switch[i].curr_position
                            neighbours.append(place_to_go)
                            # so that DICE doesn't give u same pos twice
                            pixels[jacks_diodes[place_to_go]] = colors[
                                PLAYER_COLOR(i)]

                        else:
                            pixels[jacks_diodes[place_to_go]] = colors["Wrong"]
                            while not GO_BACK(i):
                                GO_BACK(i)
                            pixels[jacks_diodes[place_to_go]] = colors["Start"]

                    else:
                        print("Error else - start anew")

                        exit(1)

                else:
                    # if both are with 0 money  its while True
                    continue
            except TypeError as e:
                CURR_STATE()
                print("ERROR: {}".format(e))
                continue
# End of Functions for beggining


# Start of Functions for main program
def DICE_2(player):
    # returns a number between 1 and 6,
    # warrant - the position it is pointing to not be a is_pressed jack
    print("Натисни черния бутон за да хвърлиш дигиталния зар")
    Button(buttons_pins['Black']).wait_for_press()
    global neigh_in_use, jacks_pins
    move_to = 6
    # move_to = choice(LAST_POS(player))
    while Button(move_to).is_pressed:
        rand = randint(1, 6)
        if jacks_pins.index(6) + rand > len(jacks_pins):
            move_to = jacks_pins[jacks_pins.index(6) + rand - len(jacks_pins)]
        else:
            move_to = jacks_pins[jacks_pins.index(6) + rand]
    return move_to


def ENEMY(player, pos):
    # if position in players arsenal
    # - returns (-1) else returns the owner of the position
    global total_players, switch
    if pos in switch[player].owned_pos:
        return -1
    else:
        for i in range(total_players):
            if pos in switch[i].owned_pos:
                return i
            if pos in switch['The game'].owned_pos:
                return 'The game'


def MQUESTION():
    questions = load(open("/home/pi/Desktop/TUESFest2019/Comp_questions.json\
        ", "r"))
    return list(questions.values())[randint(0, len(questions.values())-1)]


def PLAY_AGAIN():
    print("Край на играта, искате ли да играете отново? (Натиснете черния\
бутон за да играете отначало, червения за да не играете отново)")
    while 1:
        if Button(buttons_pins['Black']).is_pressed:
            system('clear')
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
    print("Поздравления {} ти си победител".format(switch[player].name))
    LED_START(end=switch[player].name)
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
    if switch[taker].lives <= 0:
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
        if switch[taker].money <= 0:
            print("Съжалявам, но нямаш достатъчно пари да си платиш таксата =>\
един от животите ти ще бъде отнет")
            TAKE('hp', doer, taker)
        switch[taker].money -= money
        switch[doer].money += money


def SENTENCE(to, frm='The game'):
    # this part could be made with threads
    # - gonna have better gameplay and less errors
    if frm != 'The game':
        print("{tfrm} натисни черния бутон за да оставиш {tto} безплатно\n\
        Натисни средния бутон за да вземеш 50 лв. от {tto}.\n\
        Натисни червения бутон за да вземеш 1 кръв на {tto}".format(
            tfrm=PLAYER_COLOR(frm), tto=PLAYER_COLOR(to)))
    else:
        print('{tfrm} зададе въпрос {tto} трябва да го отговори,\n\
        натисни черния бутон за да оставиш {tto} безплатно\n\
        Натисни средния бутон за да вземеш 50 лв. от {tto}.\n\
        Натисни червения бутон за да вземеш 1 кръв на {tto}'.format(
            tfrm=PLAYER_COLOR(frm), tto=PLAYER_COLOR(to)))
    try:
        while True:
            if Button(buttons_pins['Middle']).is_pressed:  # Take money
                TAKE('money', frm, to)
                sleep(0.3)
                break
            sleep(0.01)
            if Button(buttons_pins['Red']).is_pressed:  # Take HP
                TAKE('HP', frm, to)
                sleep(0.3)
                break
            sleep(0.01)
            if Button(buttons_pins['Black']).is_pressed:  # Free to go
                break
                sleep(0.3)
            sleep(0.01)
    except RuntimeError as e:
        print('RuntimeErroR: {}'.format(e))


def ASK(frm, to):

    if frm == 'The game':
        print(MQUESTION())
        SENTENCE(to)
    else:
        print('\n{} за да зададеш въпрос на {} натисни черния бутон\n\
след като отговориш трябва да решиш присъдата му\n\
дали да го оставиш, дали да му вземеш пари или кръв\n\n\
Разбира се опция е и да оставиш компютъра да зададе въпрос - \
само натисни средния бутон'.format(PLAYER_COLOR(frm), PLAYER_COLOR(to)))
        while 1:
            if Button(buttons_pins['Middle']).is_pressed:  # MQuestion
                sleep(0.1)
                print(MQUESTION())
                SENTENCE(to, frm)
                break

            elif Button(buttons_pins['Black']).is_pressed:  # I'll ask myself
                sleep(0.1)
                SENTENCE(to, frm)
                break

            else:  # Continue
                continue


def MAIN():
    global switch, neigh_in_use, colors, i, pixels  
    # its global cos i is currently the player in order to move
    while True:
        dice_res = DICE_2(i)
        # 100% there isn't another player - comes form DICE Function
        i += 1
        if i >= total_players:
            i = 0

        print("{} go To {}".format(PLAYER_COLOR(i), jacks_repr[dice_res]))
        pixels[jacks_diodes[dice_res]] = colors['Goto']

        if Button(dice_res).wait_for_press():
            neigh_in_use[i] = switch[i].curr_position
            enemy = ENEMY(i, dice_res)
            if enemy == -1:  # its my field, not enemie's
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(i)]
                continue
            elif enemy == 'The game':  # has to be went on
                print("Компютърът ще попита")
                ASK(enemy, i)
                pixels[jacks_diodes[dice_res]] = colors['Game']
            else:  # enemy field
                pixels[jacks_diodes[dice_res]] = colors[PLAYER_COLOR(enemy)]
                ASK(enemy, i)


def GAME():
    LED_START(end='Wrong')
    setup()
    LED_START(end='Game')
    print("Натисни средния бутон за да започне играта")
    Button(buttons_pins['Middle']).wait_for_press()
    LED_START()
    START()
    CURR_STATE()
    LED_START(True)
    sleep(1)
    MAIN()
    PLAY_AGAIN()


if __name__ == "__main__":
    GAME()
