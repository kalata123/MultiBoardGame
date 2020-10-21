import Snake
from gpiozero import Button


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
#    7, # tova e smeneno
    11, # na tova e smenenoto
    12,
    9
]

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
#    7: "XIV",  # на късо свързано и винаги е pushed state - hardware error
    11: "XIV - 2",
    12: "XV",
    9: "XVI",
    # Buttons
    2: "Middle Button",
    26: "Black Button",
    17: "Red Button"
}


while 1:
    for i in jacks_pins:
        if Button(i).is_active:
            print("{} - {}".format(i, jacks_repr[i]))

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
    21: 0
}
print(jacks_diodes.keys())
print(list(jacks_diodes.keys()))


# a = Snake.get_pin
