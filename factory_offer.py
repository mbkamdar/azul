# factory_offer.py

import random
from copy import deepcopy

def factory_offer(cur_player, factory_displays, center, tile_lid):
    '''
    The current player executes the factory offer phase.
    Three choices to be made:
    1. Choose a non-empty factory display or center.
    2. Choose all tiles of any one of the available colors to keep.
    3. Place the tiles on any allowed pattern lines.
    '''
    # 0. Assumes non-zero tiles in factory displays or center.

    # If human player, ask if you'd like to see your pattern lines and wall
    if type(cur_player).__name__ == "HumanPlayer":
        print(f"{cur_player.name}'s turn. Would you like to see your pattern lines and wall? (y/n)", end=' ')
        response = input()
        if response == "y":
            print("Pattern lines", " "*21, "Wall")
            print("-"*13, " "*21, "-"*4)
            for i, x in enumerate(cur_player.wall):
                print(cur_player.pattern_lines[i], " "*5, list(x.items()))
            print("\n")
    
    # 1. Put starter in center if you have the starter
    if cur_player.starter == 1:
        center['starter'] = 1
        cur_player.starter = 0
    
    # 2. Construct list of non-empty factory displays / center
    choices = [] # Create list of non-empty factory displays & center
    # Keep track of which factory_display or center is picked, hence use of i
    for i, x in enumerate(factory_displays):
        if sum(x.values()) > 0:
            choices.append((x, i))
    if sum([value for key, value in center.items() if key != 'starter']) > 0:
        choices.append(({k:v for k, v in center.items() if k != 'starter'}, 'center'))
    
    # 3. Pick from one of the choices
    # picked[0] contains the factory_display / center 
    # and picked[1] contains the location
    # chosen_color contains the color chosen from the picked choice
    # The number of chosen tiles is in picked[0][chosen_color]
    picked = cur_player.pick_factory_or_center(choices)
    color_choices = [ k for k, v in picked[0].items() if v > 0 ]
    chosen_color = cur_player.pick_color(color_choices)
    number_tiles_to_place = picked[0][chosen_color]

    # 4. Empty out the chosen factory display or center
    # 5. If picked center, take starter (if positive) & put on floor line
    
    if picked[1] == 'center': # the choice is the center
        if center['starter'] == 1:
            # become next round's starter
            cur_player.next_round_starter = 1
            # populate cur_player floor
            if len(cur_player.floor) < len(cur_player.floor_penalty):
                cur_player.floor.append('starter')
        # empty center
        for key in center.keys():
            center[key] = 0
    else: # the choice is from a factory display
        # empty factory display
        for key in factory_displays[picked[1]].keys():
            factory_displays[picked[1]][key] = 0
        
    # 6. Put remaining tiles in center, but keep starter if center w/ starter was chosen
    for k, v in picked[0].items():
        if k != chosen_color and k != 'starter':
            center[k] += v

    # 7. Put the chosen single color tiles picked on a pattern line / floor / tile_lid:
    # 7a. If a pattern line already has that color, can only place there. Excess on floor line.  If floor line is full, back in tile_lid.
    # 7b. If a wall line has that color, then corresponding pattern line cannot have that color.
    # 7c. Pick from any of the remaining pattern lines - place as many of the tiles as possible. Excess on floor line. If floor line is full, back in tile_lid.

    # place if only one option: place_on_only_option()
    placement_done, tile_lid = place_on_only_option(cur_player, chosen_color, number_tiles_to_place, tile_lid)
    
    # construct allowed pattern lines, if needed
    if not placement_done: # chosen color wasn't already on a pattern line
        allowed_lines = []
        for i, x in enumerate(cur_player.pattern_lines):
            # check if the pattern line already has a color
            if x['color'] == "none":
                # check if corresponding wall line has the chosen color
                if cur_player.wall[i][chosen_color] == 0:
                    # this line can be used
                    allowed_lines.append(i)
    
    # if no allowed lines, place all on floor
    if not placement_done:
        # if allowed_lines is null, place all on floor
        if not allowed_lines:
            placement_done, tile_lid = place_on_floor(cur_player, chosen_color, number_tiles_to_place, tile_lid)
    
    # choose from allowed pattern lines
    if not placement_done:
        if allowed_lines:
            chosen_line = cur_player.pick_pattern_line(allowed_lines)

            placement_done, tile_lid = place_on_pattern(cur_player, chosen_line, chosen_color, number_tiles_to_place, tile_lid)

    return factory_displays, center, tile_lid


def place_on_only_option(cur_player, chosen_color, number_tiles_to_place, tile_lid):
    placement_done = False
    # check if chosen color is already on a pattern line
    for i, x in enumerate(cur_player.pattern_lines):
        # yes, chosen color is already on a pattern line
        if x['color'] == chosen_color: 
            placement_done = True

            # If human player, print that all tiles can only go on this pattern line.
            if type(cur_player).__name__ == "HumanPlayer":
                print(f"All your chosen tiles can only go on pattern line {i+1}, with any overflow on the floor & lid box.\n")

            tiles_allowed = (i + 1) - x['count']
            excess_tiles = number_tiles_to_place - tiles_allowed
            # place all tiles if possible
            if excess_tiles <= 0:
                x['count'] += number_tiles_to_place
            else: # excess tiles are positive
                x['count'] = i + 1 # fill up the pattern line
                for _ in range(excess_tiles): # for each excess tile
                    if len(cur_player.floor) < 7: # place on floor if possible
                        cur_player.floor.append(chosen_color)
                    else: # else put back in lid
                        tile_lid[chosen_color] += 1

    return placement_done, tile_lid

def place_on_floor(cur_player, chosen_color, number_tiles_to_place, tile_lid):
    placement_done = True

    # If human player, print that all tiles can only go on the floor.
    if type(cur_player).__name__ == "HumanPlayer":
        print(f"All your chosen tiles can only go on the floor & lid box.\n")

    for _ in range(number_tiles_to_place): # for each tile
        if len(cur_player.floor) < 7: # place on floor if possible
            cur_player.floor.append(chosen_color)
        else: # else put back in lid
            tile_lid[chosen_color] += 1
    return placement_done, tile_lid

def place_on_pattern(cur_player, chosen_line, chosen_color, number_tiles_to_place, tile_lid):
    placement_done = True
    tiles_allowed = (chosen_line + 1) - cur_player.pattern_lines[chosen_line]['count']
    excess_tiles = number_tiles_to_place - tiles_allowed
    # place all tiles if possible
    cur_player.pattern_lines[chosen_line]['color'] = chosen_color
    if excess_tiles <= 0:
        cur_player.pattern_lines[chosen_line]['count'] += number_tiles_to_place
    else: # excess tiles are positive
        cur_player.pattern_lines[chosen_line]['count'] = chosen_line + 1 # fill up the pattern line
        for _ in range(excess_tiles): # for each excess tile
            if len(cur_player.floor) < 7: # place on floor if possible
                cur_player.floor.append(chosen_color)
            else: # else put back in lid
                tile_lid[chosen_color] += 1

    return placement_done, tile_lid

def full_factory_offer_round(players, factory_displays, center, tile_lid):
    # Initialize turn number
    turn_num = 1
    
    # Total number of colored tiles:
    total = sum([sum(x.values()) for x in factory_displays])
    total += sum(center.values()) - center['starter']

    while total > 0:
        # Print out the turn number
        print("-"*20)
        print(f"Turn number:", turn_num)
        print("-"*20)

        # Print out the current factory displays and center
        print("The current non-empty factory displays are:")
        for i, x in enumerate(factory_displays):
            if sum(x.values()) > 0:
                print(f"Factory display {i}: {x}")
        print("The center is:    ", center)
        print("-"*20)
        
        # Figure out the order in which players should start.
        # Starting from the player with the starter marker, then cycling through the rest of the list from that point forward.
        for i, cur_player in enumerate(players):
            if cur_player.starter == 1:
                starting_index = i
        new_players = players[starting_index:] + players[:starting_index]
        
        for cur_player in new_players:
            if total > 0:    
                factory_displays, center, tile_lid = factory_offer(cur_player, factory_displays, center, tile_lid)

                total = sum([sum(x.values()) for x in factory_displays])
                total += sum(center.values()) - center['starter']
        
        # Increment turn number
        turn_num += 1

    return factory_displays, center, tile_lid

# TO TEST CODE
if __name__ == "__main__":
    
    import setup_azul
    from player import Player, AIPlayer

    N = 2 # number of players, between 2 and 4
    
    # Setup the factory displays, and accordingly adjust the tile bag
    # and initialize the lid box (tile_lid) and the center
    tile_bag, tile_lid, factory_displays, center = setup_azul.setup_azul(N)

    # Create the required Player instances
    player1 = AIPlayer("Annie")
    player1.starter = 1

    player2 = AIPlayer("Megan")

    # Execute a factory offer phase for the starting player
    #factory_displays, center, tile_lid = factory_offer(player1, factory_displays, center, tile_lid)

    # Run the factory offer phase across players until no tiles left
    total = sum([sum(x.values()) for x in factory_displays])
    total += sum(center.values()) - center['starter']

    print("Initial tiles total:", total)

    while total > 0:
        factory_displays, center, tile_lid = factory_offer(player1, factory_displays, center, tile_lid)

        total = sum([sum(x.values()) for x in factory_displays])
        total += sum(center.values()) - center['starter']

        if total > 0:
            factory_displays, center, tile_lid = factory_offer(player2, factory_displays, center, tile_lid)

            total = sum([sum(x.values()) for x in factory_displays])
            total += sum(center.values()) - center['starter']
    
    print("Ensure factory displays are empty. Total:", total)
    print("New center:", center)

    print(player1.name)
    print("Pattern lines:")
    for x in player1.pattern_lines: print(x)
    print("Floor:")
    print(player1.floor)

    print(player2.name)
    print("Pattern lines:")
    for x in player2.pattern_lines: print(x)
    print("Floor:")
    print(player2.floor)

    print("New tile lid:", tile_lid)
