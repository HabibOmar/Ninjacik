import sys
import pygame
import random

from scripts.utils import load_all_images
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particles import Leaf

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Ninjacik')
        
        self.disp = pygame.display.set_mode((640, 480))
        self.window = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False, False, False]

        self.assets = load_all_images()

        self.tilemap = Tilemap(tile_assets=self.assets['Tiles'], tile_size=16)
        self.tilemap.load_map('test.json')

        self.clouds = Clouds(self.assets['Clouds'], 320, 240, count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.leaf_spawners = []
        for tree in self.tilemap.extract_tile([('Large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4+tree.pos[0], 4+tree.pos[1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract_tile([('Spawners', 0), ('Spawners', 1)]):
            if spawner.variant == 0:
                self.player.pos = spawner.pos.copy()
            else:
                self.enemies.append(Enemy(self, spawner.pos, (8, 15)))

        self.projectiles = []
        self.particles = []

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.window.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.window.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.window.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 39999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Leaf(self, pos=pos))
              

            self.clouds.update()
            self.clouds.render(self.window, offset=render_scroll)

            self.tilemap.render(self.window, offset=render_scroll)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.window, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[0] - self.movement[1], 0))
            self.player.render(self.window, offset=render_scroll)

            #[[x,y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                proj_img = self.assets['projectile']
                self.window.blit(proj_img, (projectile[0][0] - proj_img.get_width() / 2 - render_scroll[0], projectile[0][1] - proj_img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.window, offset=render_scroll)
                if kill:
                    self.particles.remove(particle)

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
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[1] = False

            self.disp.blit(pygame.transform.scale(self.window, (640, 480)), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()