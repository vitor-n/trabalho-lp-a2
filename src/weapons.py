import pygame
from utils import load_image

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = position

class Gun(Weapon):
    def __init__(self, image_path, position):
        super().__init__(image_path, position)
        self.bullets = 10

    def shoot(self):
        ...

    def update(self):
        ...

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

    def update(self):
        ...