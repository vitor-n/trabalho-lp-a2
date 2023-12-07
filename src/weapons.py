import pygame
from settings import PX_SCALE
from utils import load_image
import math
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, entity, cursor):
        super().__init__()
        self.cursor = cursor
        self.entity = entity
        self.image = load_image(image_path, PX_SCALE)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = entity.rect.center
        self.facing_r = True

    def rotate(self):
        
        """if self.recoil:
            angle_d += math.cos(5 * self.recoil_timer) * 20
        """
        self.image = pygame.transform.rotate(self.orig_image, self.cursor.angle_degrees)

        self.rect = self.image.get_rect(
            center = (math.cos(-self.cursor.angle_radians) * 80 + self.entity.rect.centerx,
                      math.sin(-self.cursor.angle_radians) * 80 + self.entity.rect.centery
                     )
        )

        if -self.cursor.angle_degrees >= 90 or -self.cursor.angle_degrees <= -90:
            if self.facing_r:
                self.orig_image = pygame.transform.flip(self.orig_image, False, True)
                self.entity.image = pygame.transform.flip(self.entity.image, True, False)
                self.facing_r = False
        
        elif not self.facing_r:
            self.orig_image = pygame.transform.flip(self.orig_image, False, True)
            self.entity.image = pygame.transform.flip(self.entity.image, True, False)
            self.facing_r = True

class Gun(Weapon):
    def __init__(self, image_path, entity, cursor):
        super().__init__(image_path, entity, cursor)
        self.bullets = 10

    def shoot(self):
        ...

    def update(self):
        self.rotate()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, angle, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path, scale)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        noise_angle = (random.random() - 0.5) / 6
        self.dx = math.cos(angle + noise_angle) * 5
        self.dy = math.sin(angle + noise_angle) * 5
        self.x = x + self.dx
        self.y = y + self.dy
        self.angle = math.degrees(angle) + 90

    def update(self):
        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.x += self.dx * 2 #+ 1 * math.sin(time/10)
        self.y += self.dy * 2 #+ 1 * math.cos(time/10)
        self.rect.center = int(self.x), int(self.y)

        #if something:
        #    self.kill()
