# draw_tiles.py

import random

def draw_tiles(factory_display, tile_bag, tile_lid):
    '''
    Randomly draws 4 tiles for a factory display from tile_bag.
    If tile_bag is empty, then tile_lid is added to tile_bag.
    If both are empty / have fewer than 4 tiles, then whatever remaining tiles are added.
    '''
    tiles = []
    num_in_factory = 4
    for key, value in tile_bag.items():
        tiles += [key]*value
    # if there aren't enough tiles, add tile_lid & empty lid
    if len(tiles) < num_in_factory:
        for key, value in tile_lid.items():
            tiles += [key]*value
            tile_bag[key] += value
        for key in tile_lid.keys():
            tile_lid[key] = 0
    # if there STILL aren't enough tiles, add all tiles
    if len(tiles) < num_in_factory:
        factory_array = tiles
    else: # there are enough tiles, so randomly sample
        factory_array = random.sample(tiles, num_in_factory)
    for x in factory_array:
        factory_display[x] += 1
        tile_bag[x] -= 1
    return factory_display, tile_bag, tile_lid