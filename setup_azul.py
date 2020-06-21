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
