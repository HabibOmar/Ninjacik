import sys
import pygame

from scripts.utils import load_all_images
from scripts.entities import Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ninjacik')
        
        self.disp = pygame.display.set_mode((640, 480))
        self.window = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False, False, False]

        self.assets = load_all_images()

        self.tilemap = Tilemap(self)
        self.tilemap.basic_map()

        self.clouds = Clouds(self.assets['Clouds'], 320, 240, count=16)

        self.player = Player(self, (50, 50), (8, 15))


        self.scroll = [0, 0]

    def run(self):
        while True:
            self.window.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.window.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.window.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.window, offset=render_scroll)

            self.tilemap.render(self.window, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[0] - self.movement[1], 0))
            self.player.render(self.window, offset=render_scroll)

            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[1] = False

            self.disp.blit(pygame.transform.scale(self.window, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()