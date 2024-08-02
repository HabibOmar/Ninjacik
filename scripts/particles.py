import random
import math

from .utils import Animation

class Particle:
    def __init__(self, animation, p_type, pos, velocity=[0,0], frame=0):
        self.animation = animation
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation.frame = frame
    
    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surf, offset=(0,0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))


class Leaf(Particle):
    def __init__(self, game, pos, velocity=[-0.1, 0.3]):
        self.pos = pos
        self.animation = Animation(game.assets['Particles']['Leaf'], img_dur=20, loop=False)
        super().__init__(self.animation, 'Leaf', self.pos, velocity, frame=random.randint(0, 20))

    def update(self):
        kill = super().update()

        self.pos[0] += math.sin(self.animation.frame * 0.035) * 0.3 

        return kill
    
    def render(self, surf, offset=(0,0)):
        super().render(surf, offset)

class Dash_Particles(Particle):
    def __init__(self, game, pos, velocity=[0, 0]):
        self.pos = pos
        self.animation = Animation(game.assets['Particles']['Particle'], img_dur=6, loop=False)
        super().__init__(self.animation, 'Particle', self.pos, velocity, frame=random.randint(0, 7))

    def update(self):
        kill = super().update()
        return kill
    
    def render(self, surf, offset=(0,0)):
        super().render(surf, offset)

 