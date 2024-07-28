import pygame

class PhysicsEntinty:
    def __init__(self, game, e_type, pos, size, color=None):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.color = color
        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
    
    def render(self, surf):
        surf.blit(self.game.assets[self.e_type], self.pos)