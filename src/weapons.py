import pygame
from settings import PX_SCALE
from utils import load_image
import math

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, position, cursor):
        super().__init__()
        self.cursor = cursor
        self.image = load_image(image_path, PX_SCALE)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def rotate(self):
        
        """if self.recoil:
            angle_d += math.cos(5 * self.recoil_timer) * 20
        """
        self.image = pygame.transform.rotate(self.orig_image, self.cursor.angle_degrees)

        self.rect = self.image.get_rect(center=(math.cos(-self.cursor.angle_radians) * 30 + 640,
                                                math.sin(-self.cursor.angle_radians) * 30 + 360))

        #if -angle_d >= 90 or -angle_d <= -90:
        #    if self.facing_r:
        #        self.orig_image = pygame.transform.flip(
        #            self.orig_image, False, True)
        #        player.image = pygame.transform.flip(player.image, True, False)
        #        self.facing_r = False
        #
        #elif not self.facing_r:
        #    self.orig_image = pygame.transform.flip(
        #        self.orig_image, False, True)
        #    player.image = pygame.transform.flip(player.image, True, False)
        #    self.facing_r = True

class Gun(Weapon):
    def __init__(self, image_path, position, cursor):
        super().__init__(image_path, position, cursor)
        self.bullets = 10

    def shoot(self):
        ...

    def update(self):
        self.rotate()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

    def update(self):
        ...