# azul.py

# Game engine to play Azul

from player import create_human_players, create_AI_players, starting_player
from setup_azul import setup_azul
from draw_tiles import draw_tiles
from factory_offer import full_factory_offer_round
from wall_tiling import wall_tiling
from game_end_scoring import check_game_end, final_scoring

def play_azul(N, num_human, num_AI):
    '''
    Play the game
    '''
    
    # Setup the factory displays, and accordingly adjust the tile bag
    # and initialize the lid box (tile_lid) and the center
    tile_bag, tile_lid, factory_displays, center = setup_azul(N)

    # Create the required Player instances
    human_players = create_human_players(num_human)
    AI_players = create_AI_players(num_AI)
    players = human_players + AI_players

    # Print out the names of all players
    if num_human >= 1:
        print_player_names(human_players)
    if num_AI >= 1:
        print_player_names(AI_players)

    # Randomly choose the starting player
    x = starting_player(players)

    # Play the game
    game_end = 0
    round_num = 1
    while not game_end:
        # Print round number
        print("#"*40)
        print("#", f"ROUND {round_num}".center(36), "#")
        print("#"*40)
        
        # Print the name of the starting player
        for x in players:
            if x.starter == 1:
                print(f"The starting player is:", x.name, "\n")
        
        # Execute the factory offer phase until no tiles left
        factory_displays, center, tile_lid = full_factory_offer_round(players, factory_displays, center, tile_lid)
        
        # Do the wall tiling phase
        tile_lid = wall_tiling(players, tile_lid)

        # Print each player's score, pattern lines, and wall
        print("-"*10)
        print(f"END OF ROUND {round_num}.")
        print("Each player's pattern lines and wall are as follows:")
        for cur_player in players:
            print("~"*10)
            print(cur_player.name)
            print("~"*10)
            print("Pattern lines", " "*21, "Wall")
            print("-"*13, " "*21, "-"*4)
            for i, x in enumerate(cur_player.wall):
                print(cur_player.pattern_lines[i], " "*5, list(x.items()))
        print("\nThe current player scores are:")
        for x in players:
            print(f"{x.name}: {x.score}")
        print("+"*10)
        input("Press Enter to continue...")

        # Increment round number
        round_num += 1

        # Check if game should end
        game_end = check_game_end(players)

        # Draw a new set of tiles in the factory displays
        for x in factory_displays:
            x, tile_bag, tile_lid = draw_tiles(x, tile_bag, tile_lid)
    
    winners = final_scoring(players)
    print("#"*40)
    print("#", "GAME END".center(36), "#")
    print("#"*40)
    print("Final scores are:")
    for cur_player in players:
        print(cur_player.name, "Score:", cur_player.score)
    if len(winners) == 1:
        print("Winner is", winners[0].name)
    else:
        print("Winners are", [cur_player.name for cur_player in winners])

def print_player_names(players):
    class_type = type(players[0]).__name__
    string = class_type[:class_type.find("Player")] + " " + "Player"
    if len(players) == 1:
        print(f"The {string} is: {players[0].name}")
    if len(players) > 1:
        print(f"The {string}s are: ", end='')
        print(', '.join(x.name for x in players))

   
if __name__ == "__main__":

    # Ask for # of players
    N = int(input("Choose # of players (between 2 and 4): "))
    num_human = int(input("How many of these are human players: "))
    num_AI = N - num_human

    play_azul(N, num_human, num_AI)
