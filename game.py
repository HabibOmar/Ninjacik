import sys
import pygame

from scripts.utils import load_image
from scripts.entities import PhysicsEntinty

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ninjacik')
        
        self.full_window = pygame.display.set_mode((640, 480))
        self.half_window = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False, False, False]

        self.assets = {
            'player': load_image('entities/player.png')
        }

        self.player = PhysicsEntinty(self, 'player', (50, 50), (8, 15))

    def run(self):
        while True:
            self.half_window.fill((14, 219, 248))

            self.player.update((self.movement[2] - self.movement[3], 0))
            self.player.render(self.half_window)

            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[2] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[2] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[3] = False

            self.full_window.blit(pygame.transform.scale(self.half_window, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()