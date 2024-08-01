import pygame
from .utils import Animation

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, image, animation_cache=None):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.image = image
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.animation_cache = animation_cache
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('Idle')

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

        self.velocity[1] = min(self.velocity[1] + 0.1, 5)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        self.animation.update()
    
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        self.animation_cache = {'Idle': Animation(game.assets['Entities']['Player']['Idle']), 
                           'Run': Animation(game.assets['Entities']['Player']['Run']), 
                           'Jump': Animation(game.assets['Entities']['Player']['Jump']),
                           'Slide': Animation(game.assets['Entities']['Player']['Slide']),
                           'Wall_slide': Animation(game.assets['Entities']['Player']['Wall_slide'])}
        super().__init__(game, 'Player', pos, size, game.assets['Entities']['player'], animation_cache=self.animation_cache)
        self.air_time = 0
    
    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('Jump')
        elif movement[0] != 0:
            self.set_action('Run')
        else:
            self.set_action('Idle')
