import pygame
from settings import PX_SCALE
from utils import load_image
import math
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, cursor):
        super().__init__()
        self.cursor = cursor
        self.image = load_image(image_path, PX_SCALE)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.facing_r = True

    def set_entity(self, entity):
        self.entity = entity
        self.rect.center = entity.rect.center

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, self.cursor.angle_degrees)

        self.rect = self.image.get_rect(
            center = (math.cos(-self.cursor.angle_radians) * 65 + self.entity.rect.centerx,
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
    def __init__(self, image_path, cursor):
        super().__init__(image_path, cursor)
        self.bullets = 10
        self.bullet_group = pygame.sprite.Group()

    def shoot(self):
        print("Bang!!!\n")

        bullet = Bullet(("..", "trabalho-lp-a2", "Sprites", "bullets", "bullet1.png"), (self.rect.centerx, self.rect.centery), self.cursor.angle_radians)
        self.bullet_group.add(bullet)

    def update(self):
        self.rotate()
        self.bullet_group.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path, PX_SCALE)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.dx = math.cos(-angle)
        self.dy = math.sin(-angle)

        self.angle = math.degrees(angle) + 90

        self.time = 0

    def update(self):
        self.time += 1
        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.centerx += self.dx * 2 + 0 * math.sin(self.time/10)
        self.rect.centery += self.dy * 2 + 0 * math.cos(self.time/10)

        #if self.rect.centerx > 1000 or self.rect.centerx < 0 or self.rect.centery < 0 or self.rect.centery > 1000:
        #    self.kill()

