import pygame

NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0)]
PHYSICS_TILES = {'Grass', 'Stone'}

class Tile:
    def __init__(self, type, variant, pos):
        self.type = type
        self.variant = variant
        self.pos = pos

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.assets = game.assets
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
    
    def basic_map(self):
        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = Tile(type='Grass', variant='1', pos=(3+i, 10))
            self.tilemap['10;' + str(5+i)] = Tile(type='Stone', variant='1', pos=(10, 5+i))

    def neighbor_tiles(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for neighbor in NEIGHBORS:
            check_loc = str(tile_loc[0] + neighbor[0]) + ';' + str(tile_loc[1] + neighbor[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.neighbor_tiles(pos):
            if tile.type in PHYSICS_TILES:
                rects.append(pygame.Rect(tile.pos[0] * self.tile_size, tile.pos[1] * self.tile_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.assets['Tiles'][tile.type][tile.variant], (tile.pos[0] - offset[0], tile.pos[1] - offset[1]))

        for location in self.tilemap:
            tile = self.tilemap[location]
            surf.blit(self.assets['Tiles'][tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
        