import os
import pygame

BASE_IMAGE_PATH = 'data/images/'

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
                
                d = images
                for part in parts[:-1]:
                    if part not in d:
                        d[part] = {}
                    d = d[part]
                d[parts[-1][:-4]] = image
                
    return images


# pygame.init()
# pygame.display.set_mode((640, 480))
# imgs = load_all_images()
# print(imgs['Tiles']['Grass']['1'])