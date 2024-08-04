import os

import pygame

BASE_IMAGE_PATH = 'data/images/'
BASE_SFX_PATH = 'data/sfx/'

def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_all_images(BASE_IMAGE_PATH=BASE_IMAGE_PATH):
    images = {}
    
    for root, _, files in os.walk(BASE_IMAGE_PATH):
        for file in files:
            if file.endswith('.png'):
                full_path = os.path.join(root, file)
                image = pygame.image.load(full_path).convert()
                image.set_colorkey((0, 0, 0))
                
                # Creating a nested dictionary structure
                relative_path = os.path.relpath(full_path, BASE_IMAGE_PATH)
                parts = relative_path.split(os.sep)
                
                key = parts[-1][:-4]
                try:
                    key = int(key)
                except ValueError:
                    pass

                d = images
                for part in parts[:-1]:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                d[key] = image
    return images

def load_all_sfx(BASE_SFX_PATH=BASE_SFX_PATH):
    sfx = {}

    pygame.mixer.init()

    for file in os.listdir(BASE_SFX_PATH):
        if file.endswith('.wav'):
            full_path = os.path.join(BASE_SFX_PATH, file)
            sfx[file[:-4]] = pygame.mixer.Sound(full_path)
    return sfx

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        
        self.frame = 0
        self.done = False
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (len(self.images) * self.img_duration)
        else:
            self.frame = min(self.frame + 1 , self.img_duration * len(self.images) - 1)
            if self.frame == len(self.images) * self.img_duration - 1:
                self.done = True

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def img(self):
        return self.images[int(self.frame / self.img_duration)]