# wall_tiling.py

def wall_tiling(players, tile_lid):
    '''
    All players execute the wall tiling phase & the corresponding scoring phase.
    '''
    # For each player:
    for cur_player in players:
        for i, x in enumerate(cur_player.pattern_lines):
            # 1. If pattern line is complete, fill the corresponding color on the wall.
            if x['count'] == (i + 1):
                old_list = list(cur_player.wall[i].values())
                cur_player.wall[i][x['color']] = 1

                # 2. Move remaining tiles from the pattern line to the tile_lid.
                tile_lid[x['color']] += x['count'] - 1
                x['count'] = 0
                x['color'] = 'none'

                # 3. Score the tile placed on the wall.
                # Create matrix from wall dictionary
                wall_count = []
                for x in cur_player.wall:
                    wall_count.append(list(x.values()))

                # Get index of placed tile.
                # Necessary because key of orderedDict doesn't remember index.
                new_list = list(cur_player.wall[i].values())
                placed_tile = [e2 - e1 for (e1, e2) in zip(old_list, new_list)]
                placed_tile_index = placed_tile.index(1)

                # Construct lists of numbers above, below, left and right of the placed tile.
                # Reverse the list that's to the left and above to make it easy to traverse until 0.
                left = wall_count[i][:placed_tile_index]
                left_reversed = left[::-1]
                right = wall_count[i][(placed_tile_index+1):]

                col = [row[placed_tile_index] for row in wall_count]
                above = col[:i]
                above_reversed = above[::-1]
                below = col[(i+1):]

                # Score the tiles to each side of the placed_tile
                score_left = score_function(left_reversed)
                score_right = score_function(right)
                score_above = score_function(above_reversed)
                score_below = score_function(below)

                # Increment the current player's score
                cur_player.score += (1 + score_left + score_right + score_above + score_below)

        # Score the floor penalties
        score_floor = sum(cur_player.floor_penalty[:len(cur_player.floor)])
        cur_player.score += score_floor

        # If you are the next round starter, then become starter
        if cur_player.next_round_starter == 1:
            cur_player.starter = 1
            cur_player.next_round_starter = 0

        # Put the floor tiles back into the lid, except the 'starter'
        for x in cur_player.floor:
            if x != 'starter':
                tile_lid[x] += 1

        # Empty the floor
        cur_player.floor = []
    
    return tile_lid

# Given an array, returns the sum of all items until 0
# If empty, score = 0; if no zeroes, sum all items
def score_function(array):
    score = 0
    if array:
        if 0 in array:
            score = sum(array[:array.index(0)])
        else:
            score = sum(array)
    return score