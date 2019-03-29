# File only for classes

class Player:

    owned_pos = []

    def __init__(self, start_lives = 3, start_money = 1000, position = None):
        self.position = position
        self.lives = start_lives
        self.money = start_money

    def __str__(self):
        return "Player on {} position with {} lives and {}$".format(self.position, self.lives, self.money)

    def PAY(self, money_to_pay):
        self.money -= money_to_pay

    def LOSE_HP(self, hp_to_lose = 1):
        self.lives -= hp_to_lose

    def NEW_POSITION(self, new_pos):
        self.position = new_pos

class Board:

    def __init__(self, jacks_pins, buttons_pins, neighbours = None):
        self.jacks_pins = jacks_pins
        self.buttons_pins = buttons_pins
        self.neighbours = neighbours

    def ADD_NEIGHBOUR(self, n_pos):
        # n_pos == neightbour position
        # appends it to the table if its not in it
        if n_pos not in self.neighbours:
            self.neighbours.append(n_pos)
        else:
            pass

    def REMOVE_NEIGHBOUR(self, n_pos):
        # removes neigh_position if in neighbours
        if n_pos in self.neighbours:
            self.neighbours.remove(i)
        else:
            pass
