# setup_azul.py

from draw_tiles import draw_tiles

def setup_azul(N):
    '''
    Initial board and tile setup
    '''
    # Construct tiles: dictionary of tiles: key = color, value = number 
    # All tiles are either in a bag or the lid,
    # or each player's pattern lines or wall
    tile_bag = {'blue': 20, 
            'yellow': 20, 
            'red': 20, 
            'black': 20, 
            'white': 20}
    tile_lid = {'blue': 0, 
            'yellow': 0, 
            'red': 0, 
            'black': 0, 
            'white': 0}

    # Construct factory displays
    num_of_factories = 2*N + 1
    factory_displays = []
    for _ in range(num_of_factories):
        factory_displays.append({'blue': 0, 
                                'yellow': 0, 
                                'red': 0, 
                                'black': 0, 
                                'white': 0})

    # Construct center
    # Start game with no tiles in center
    center = {'blue': 0, 
            'yellow': 0, 
            'red': 0, 
            'black': 0, 
            'white': 0, 
            'starter': 0}
    
    # For each factory display, populate randomly & accordingly adjust tile_bag
    for i in range(num_of_factories):
        factory_displays[i], tile_bag, tile_lid = draw_tiles(factory_displays[i], tile_bag, tile_lid)

    return tile_bag, tile_lid, factory_displays, center
 
# To test code
if __name__ == "__main__":
    N = 2 # number of players, between 2 and 4
    
    tile_bag, tile_lid, factory_displays, center = setup_azul(N)
    
    print("Tile bag:", tile_bag)
    print("Tiles in bag:", sum(tile_bag.values()))
    print("Factory displays:")
    for i, x in enumerate(factory_displays):
        print("Factory display", i, ":", x)
    print("Tile lid:", tile_lid)

    # Test case 1
    # empty factory displays
    for x in factory_displays:
        for key in x.keys():
            x[key] = 0
    # run draw_tiles2 for each factory display
    for i, x in enumerate(factory_displays):
        x, tile_bag, tile_lid = draw_tiles(x, tile_bag, tile_lid)
    
    print("-"*40)
    print("Tile bag:", tile_bag)
    print("Tiles in bag:", sum(tile_bag.values()))
    print("Factory displays:")
    for i, x in enumerate(factory_displays):
        print("Factory display", i, ":", x)
    print("Tile lid:", tile_lid)

    # Test case 2
    # empty factory displays
    for x in factory_displays:
        for key in x.keys():
            x[key] = 0
    # artificially have insufficient tiles in bag
    tile_bag = {'blue': 4, 
            'yellow': 4, 
            'red': 4, 
            'black': 3, 
            'white': 0}
    # inadequate even in tile_lid
    tile_lid = {'blue': 0, 
            'yellow': 0, 
            'red': 0, 
            'black': 0, 
            'white': 0}
    # run draw_tiles2
    for i, x in enumerate(factory_displays):
        x, tile_bag, tile_lid = draw_tiles(x, tile_bag, tile_lid)
    
    print("-"*40)
    print("Tile bag:", tile_bag)
    print("Tiles in bag:", sum(tile_bag.values()))
    print("Factory displays:")
    for i, x in enumerate(factory_displays):
        print("Factory display", i, ":", x)
    print("Tile lid:", tile_lid)