import sys

import pygame

from scripts.utils import load_all_images
from scripts.tilemap import Tile, Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ninjacik')
        
        self.disp = pygame.display.set_mode((640, 480))
        self.disp = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False, False, False]

        self.tile_assets = load_all_images('data/images/Tiles/')

        self.tilemap = Tilemap(tile_assets=self.tile_assets, tile_size=16)

        try:
            self.tilemap.load_map('test.json')
        except FileNotFoundError as e:
            print("No map found:", e)
        except Exception as e:
            print("Error loading map:", e)

        self.scroll = [0, 0]

        self.tiles_list = list(self.tile_assets)
        self.tile_type = 0
        self.tile_variant = 0
        self.on_grid = True

        self.l_click = False
        self.r_click = False
        self.shift = False

    def run(self):
        while True:
            self.disp.fill((0,0,0))

            self.scroll[0] += (self.movement[0] - self.movement[1]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.disp, offset=render_scroll)
            
            curr_tile = self.tile_assets[self.tiles_list[self.tile_type]][self.tile_variant].copy()
            curr_tile.set_alpha(128)

            m_pos = pygame.mouse.get_pos()
            m_pos = (m_pos[0] / RENDER_SCALE, m_pos[1] / RENDER_SCALE)
            tile_pos = (int((m_pos[0] + self.scroll[0]) // self.tilemap.tile_size), int((m_pos[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.on_grid: 
                self.disp.blit(curr_tile,(tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.disp.blit(curr_tile, m_pos)

            if self.l_click and self.on_grid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = Tile(type=self.tiles_list[self.tile_type], variant=self.tile_variant, pos=tile_pos)
            if self.r_click:
                if str(tile_pos[0]) + ';' + str(tile_pos[1]) in self.tilemap.tilemap:
                    del self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])]
                for tile in self.tilemap.offgrid_tiles:
                    tile_img = self.tile_assets[tile.type][tile.variant]
                    if pygame.Rect(tile.pos[0] - self.scroll[0], tile.pos[1] - self.scroll[1], tile_img.get_width(), tile_img.get_height()).collidepoint(m_pos):
                        self.tilemap.offgrid_tiles.remove(tile)
                    

            self.disp.blit(curr_tile, (5, 5))

            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.l_click = True
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append(Tile(type=self.tiles_list[self.tile_type], variant=self.tile_variant, pos=(m_pos[0] + self.scroll[0], m_pos[1] + self.scroll[1])))
                    if event.button == 3:
                        self.r_click = True
                    if not self.shift:
                        if event.button == 4:
                            self.tile_type = (self.tile_type - 1) % len(self.tiles_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_type = (self.tile_type + 1) % len(self.tiles_list)
                            self.tile_variant = 0
                    else:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.tile_assets[self.tiles_list[self.tile_type]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.tile_assets[self.tiles_list[self.tile_type]])

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.l_click = False
                    if event.button == 3:
                        self.r_click = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid
                    if event.key == pygame.K_r:
                        self.tilemap.offgrid_tiles = []
                        self.tilemap.tilemap = {}
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save_map('test.json')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                    if event.key == pygame.K_a:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = False

            self.disp.blit(pygame.transform.scale(self.disp, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()