import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('A Game')

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0))

        self.img_pos = [100, 200]
        self.movement = [False, False, False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.window.fill((14, 219, 248))

            self.img_pos[0] += (self.movement[2] - self.movement[3]) * 5
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5

            self.window.blit(self.img, self.img_pos)

            img_r = pygame.Rect(*self.img_pos, *self.img.get_size())

            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.window, (225, 10, 72), self.collision_area)
            else:
                pygame.draw.rect(self.window, (100, 10, 25), self.collision_area)

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

            pygame.display.update()
            self.clock.tick(60)

Game().run()