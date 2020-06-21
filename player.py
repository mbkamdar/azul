# player.py

# Class definition for each player

from collections import OrderedDict
from copy import deepcopy
import random

class Player:
    '''
    An instance for each player
    '''
    def __init__(self, name):
        self.name = name
        self.starter = 0
        self.next_round_starter = 0
        self.score = 0
        #self.filled_lines = 0
        
        # Wall stored as an ordered dict
        wall = [OrderedDict({'blue': 0, 'yellow': 0, 'red': 0, 'black': 0, 'white': 0}), 
                OrderedDict({'white': 0, 'blue': 0, 'yellow': 0, 'red': 0, 'black': 0}), 
                OrderedDict({'black': 0, 'white': 0, 'blue': 0, 'yellow': 0, 'red': 0}), 
                OrderedDict({'red': 0, 'black': 0, 'white': 0, 'blue': 0, 'yellow': 0}), 
                OrderedDict({'yellow': 0, 'red': 0, 'black': 0, 'white': 0, 'blue': 0})]

        # Pattern Line as list of dicts containing color and count
        pattern_lines = [{'color': 'none', 'count': 0}, 
                        {'color': 'none', 'count': 0}, 
                        {'color': 'none', 'count': 0}, 
                        {'color': 'none', 'count': 0}, 
                        {'color': 'none', 'count': 0}]
        
        # Floor as list of None elements (no more than 7 elements allowed)
        # Floor penalty as a list of associated penalties
        floor = []
        floor_penalty = [-1, -1, -2, -2, -2, -3, -3]

        self.wall = wall
        self.pattern_lines = pattern_lines
        self.floor = floor
        self.floor_penalty = floor_penalty

class AIPlayer(Player):
    def pick_factory_or_center(self, choices):
        picked = random.choice(choices)
        picked = deepcopy(picked)
        print(f"\n{self.name}'s choice is: {picked}", end='; ')
        return picked

    def pick_color(self, color_choices):
        chosen_color = random.choice(color_choices)
        print(f"the {chosen_color} tiles(s).\n")
        return chosen_color

    def pick_pattern_line(self, allowed_lines):
        chosen_line = random.choice(allowed_lines)
        return chosen_line

class HumanPlayer(Player):
    def pick_factory_or_center(self, choices):
        print("Your choices are:")
        for i, x in enumerate(choices):
            print(f"Choice number {i}: {x}")
        choice = int(input("Enter choice number: "))
        picked = choices[choice]
        picked = deepcopy(picked)
        print(f"You picked: {picked}")
        return picked

    def pick_color(self, color_choices):
        print("And from these colored tiles:", color_choices)
        chosen_color = input("Pick a color: ")
        return chosen_color

    def pick_pattern_line(self, allowed_lines):
        print("Your pattern lines are:")
        for i, x in enumerate(self.pattern_lines):
            print(f"Pattern line {i+1}: {x}")
        print(f"Allowed lines are ", end='')
        print([x+1 for x in allowed_lines])
        chosen_line = int(input("Pick from allowed line: ")) - 1
        return chosen_line

def create_AI_players(num = 0):
    '''
    Initial AI player construction
    '''
    AI_players = []
    if num >= 1:
        AI_players.append(AIPlayer("Andrew"))
    if num >= 2:
        AI_players.append(AIPlayer("Bob"))
    if num >= 3:
        AI_players.append(AIPlayer("David"))
    if num == 4:
        AI_players.append(AIPlayer("John"))
    return AI_players

def create_human_players(num = 0):
    '''
    Initial Human player construction
    '''
    human_players = []
    for i in range(num):
        print(f"Player {i+1}'s name: ", end='')
        name = input()
        human_players.append(HumanPlayer(name))
    return human_players

def starting_player(players):
    '''
    Randomly choose the starting player, 
    and return the index of starting player
    '''
    x = random.randint(0, len(players)-1)
    players[x].starter = 1
    return x

# To test code
if __name__ == "__main__":
    player1 = Player("Annie")
    print(player1.name)
    print("Starter?", player1.starter)
    print("Score =", player1.score)
    print("Wall:")
    for x in player1.wall:
        print(list(x.items()))
    print("Pattern Lines:")
    for x in player1.pattern_lines:
        print(x)
    print("Floor:")
    print(player1.floor)