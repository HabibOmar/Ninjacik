import pygame

class Tile:
    def __init__(self, type, variant, position):
        self.type = type
        self.variant = variant
        self.position = position

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.assets = game.assets
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
    
    def basic_map(self):
        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = Tile(type='Grass', variant='1', position=(3+i, 10))
            self.tilemap['10;' + str(5+i)] = Tile(type='Stone', variant='1', position=(10, 5+i))
    
    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.assets['Tiles'][tile.type][tile.variant], tile.position)

        for location in self.tilemap:
            tile = self.tilemap[location]
            surf.blit(self.assets['Tiles'][tile.type][tile.variant], (tile.position[0] * self.tile_size, tile.position[1] * self.tile_size))
        