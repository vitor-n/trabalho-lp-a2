import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = position

class Gun(Weapon):
    def __init__(self, image_path, position):
        super().__init__(image_path, position)
        self.bullets = 10

    def shoot(self):
        ...

