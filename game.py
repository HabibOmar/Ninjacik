import sys
import os
import pygame
import random
import math

from scripts.utils import load_all_images
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particles import Leaf, Particles
from scripts.spark import Spark

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

        self.clouds = Clouds(self.assets['Clouds'], 320, 240, count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.screenshake = 0

        self.level = 0
        self.load_level(self.level)
    
    def load_level(self, level_id):
        self.tilemap.load_map(f'data/maps/{str(level_id)}.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract_tile([('Large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4+tree.pos[0], 4+tree.pos[1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract_tile([('Spawners', 0), ('Spawners', 1)]):
            if spawner.variant == 0:
                self.player.pos = spawner.pos.copy()
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner.pos, (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    def run(self):
        while True:
            self.window.blit(self.assets['background'], (0,0))

            self.screenshake = max(0, self.screenshake - 1)

            if not self.enemies and not self.dead:
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(self.transition + 1, 30)
                if self.dead > 50:
                    self.load_level(self.level)

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
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.window, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
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
                    for _ in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(self.screenshake, 16)
                        for _ in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particles(self, self.player.rect().center, [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5]))
            
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.window, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
                    
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
            
            if self.transition:
                transition_surf = pygame.Surface(self.window.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.window.get_width() // 2, self.window.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.window.blit(transition_surf, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.disp.blit(pygame.transform.scale(self.window, (640, 480)), screenshake_offset)
            pygame.display.update()
            self.clock.tick(60)

Game().run()