# game_end_scoring.py

def check_game_end(players):
    '''
    Checks if game should end, if a horizontal line on the wall is complete.
    '''
    game_end = 0
    for cur_player in players:
        for x in cur_player.wall:
            if sum(x.values()) == 5:
                game_end += 1
    return game_end

def final_scoring(players):
    '''
    End of game scoring, and winner declaration
    '''
    for cur_player in players:
           
        # 1. Score 2 pts for each complete horizontal line.
        for x in cur_player.wall:
            if sum(x.values()) == 5:
                cur_player.score += 2

        # 2. Score 7 pts for each complete vertical line.
        wall_values = []
        for x in cur_player.wall:
            wall_values.append(list(x.values()))
        cols = []
        for i in range(len(wall_values)):
            cols.append([row[i] for row in wall_values])

        for x in cols:
            if sum(x) == 5:
                cur_player.score += 7

        # 3. Score 10 pts if all 5 tiles of a color are filled.
        for color in cur_player.wall[0].keys():
            color_sum = sum([x[color] for x in cur_player.wall])
            if color_sum == 5:
                cur_player.score += 10
    
    # Find winner
    max_score = max([cur_player.score for cur_player in players])
    top_scorers = [cur_player for cur_player in players if cur_player.score == max_score]

    # Add # of completed horizontal lines for each player
    for cur_player in players:
        filled_lines = 0
        for x in cur_player.wall:
            if sum(x.values()) == 5:
                filled_lines += 1
        cur_player.filled_lines = filled_lines

    if len(top_scorers) == 1:
        winners = top_scorers
    else: # if multiple top scorers
        # for each top_scorer, check who has the most horizontal lines
        max_filled_lines = max([cur_player.filled_lines for cur_player in top_scorers])
        most_filled_lines = [cur_player for cur_player in top_scorers if cur_player.filled_lines == max_filled_lines]
        winners = most_filled_lines
    
    return winners