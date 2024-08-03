import pygame
import math
import random

from .utils import Animation
from .particles import Dash_Particles

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, animation_cache=None):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.animation_cache = animation_cache
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('Idle')
        self.last_movement = (0, 0)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if self.action != action:
            self.action = action
            if action in self.animation_cache:
                self.animation = self.animation_cache[action]
                if not self.animation.loop and self.animation.done:
                    self.animation = self.animation.copy()
                    self.animation_cache[action] = self.animation

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True 
                elif frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]

        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                elif frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True
        
        self.last_movement = movement

        self.velocity[1] = min(self.velocity[1] + 0.1, 5)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.animation.update()
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size,):
        self.animation_cache = {'Idle': Animation(game.assets['Entities']['Enemy']['Idle']), 
                           'Run': Animation(game.assets['Entities']['Enemy']['Run'])}
        
        super().__init__(game, 'Enemy', pos, size, animation_cache=self.animation_cache)

        self.walking = 0
        self.gun = game.assets['gun']

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if self.collisions['right'] or self.collisions['left'] or not(tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23))):
                self.flip = not self.flip
            else:
                movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            self.walking = max(0, self.walking - 1)

        elif random.random() < 0.01:
            self.walking = random.randint(30, 60)
            # if random.random() < 0.5:
            #     self.velocity[0] = 1
            # else:
            #     self.velocity[0] = -1
        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('Run')
        else:
            self.set_action('Idle')

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.gun, True, False), (self.rect().centerx - 4 - self.gun.get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surf.blit(self.gun, (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.animation_cache = {'Idle': Animation(game.assets['Entities']['Player']['Idle']), 
                           'Run': Animation(game.assets['Entities']['Player']['Run']), 
                           'Jump': Animation(game.assets['Entities']['Player']['Jump']),
                           'Slide': Animation(game.assets['Entities']['Player']['Slide']),
                           'Wall_slide': Animation(game.assets['Entities']['Player']['Wall_slide'])}
        
        super().__init__(game, 'Player', pos, size, animation_cache=self.animation_cache)
        
        self.air_time = 0
        self.jumps = 2
        self.dashing = 0
    
    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2
            self.wall_slide = False
        
        self.wall_slide = False
        if self.collisions['left'] or self.collisions['right'] and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('Wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('Jump')
            elif movement[0] != 0:
                self.set_action('Run')
            else:
                self.set_action('Idle')
        
        if abs(self.dashing) in {60, 50}:
            for _ in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                p_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Dash_Particles(self.game, self.rect().center, velocity=p_velocity))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        elif self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            p_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Dash_Particles(self.game, self.rect().center, velocity=p_velocity))
        

            
        if self.velocity[0] > 0:
            self.velocity[0] = max(0, self.velocity[0] - 0.1)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(0, self.velocity[0] + 0.1)
    
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)
    
    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.jumps -= 1
            self.velocity[1] = -3
            self.air_time = 5
            return True
            
    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
