import json

import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
AUTOTILE_TYPES = {'Grass', 'Stone'}
AUTOTILE_OFFSETS = [(1, 0), (-1, 0), (0, -1), (0, 1)]

NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1), (0, 0)]
PHYSICS_TILES = {'Grass', 'Stone'}

class Tile:
    def __init__(self, type, variant, pos):
        self.type = type
        self.variant = variant
        self.pos = pos
    
    def to_dict(self):
        return {'type': self.type, 'variant': self.variant, 'pos': self.pos}

class Tilemap:
    def __init__(self, tile_assets, tile_size = 16):
        self.assets = tile_assets
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
    
    def basic_map(self):
        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = Tile(type='Grass', variant=1, pos=(3+i, 10))
            self.tilemap['10;' + str(5+i)] = Tile(type='Stone', variant=1, pos=(10, 5+i))
    
    def save_map(self, path):
        file = open(path, 'w')
        serialized_tilemap = {key : self.tilemap[key].to_dict() for key in self.tilemap}
        serialized_offgrid_tiles = [tile.to_dict() for tile in self.offgrid_tiles]
        json.dump({'tilemap': serialized_tilemap, 'offgrid_tile': serialized_offgrid_tiles ,'tile_size': self.tile_size}, file)
        file.close()
    
    def load_map(self, path):
        file = open(path, 'r')
        map_data = json.load(file)
        self.tile_size = map_data['tile_size']
        self.tilemap = {key : Tile(**map_data['tilemap'][key]) for key in map_data['tilemap']}
        self.offgrid_tiles = [Tile(**tile) for tile in map_data['offgrid_tile']]
        file.close()

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
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]

            if tile.type not in AUTOTILE_TYPES:
                continue

            neighbors = set()
            for shift in AUTOTILE_OFFSETS:
                check_loc = str(tile.pos[0] + shift[0]) + ';' + str(tile.pos[1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc].type == tile.type:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if neighbors in AUTOTILE_MAP:
                tile.variant = AUTOTILE_MAP[neighbors]
                

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.assets[tile.type][tile.variant], (tile.pos[0] - offset[0], tile.pos[1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.assets[tile.type][tile.variant], (tile.pos[0] * self.tile_size - offset[0], tile.pos[1] * self.tile_size - offset[1]))
        