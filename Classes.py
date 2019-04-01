# File only for classes

class Player():

    def __init__(self, name, start_lives = 3, start_money = 1000, position = None):
        self.name = name
        self.curr_position = position
        self.lives = start_lives
        self.money = start_money
        self.owned_pos = []

    def __str__(self):
        return '''Player {:6} on position {:2} with {} lives and {:3}$ and \
{} positions'''.format(self.name, self.curr_position, \
        self.lives, self.money, self.owned_pos)

    def ADD_POSITION(self, new_pos, money_to_pay):
        if self.money >= money_to_pay:
            self.money = self.money - money_to_pay
            self.owned_pos.append(new_pos)
            self.curr_position = new_pos
            return 1
        else:
            return -1

    def LOSE_HP(self, hp_to_lose = 1):
        self.lives -= hp_to_lose
