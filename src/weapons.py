import pygame
from settings import PX_SCALE
from utils import load_image
import math
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path, target):
        super().__init__()
        self.target = target
        self.image = load_image(image_path)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.facing_r = True

    def set_entity(self, entity):
        self.entity = entity
        self.rect.center = entity.rect.center

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, self.target.angle_degrees)

        self.rect = self.image.get_rect(
            center = (math.cos(-self.target.angle_radians) * 65 + self.entity.rect.centerx,
                      math.sin(-self.target.angle_radians) * 80 + self.entity.rect.centery
                    )
                    )

        if -self.target.angle_degrees >= 90 or -self.target.angle_degrees <= -90:
            if self.facing_r:
                self.orig_image = pygame.transform.flip(self.orig_image, False, True)
                self.entity.image = pygame.transform.flip(self.entity.image, True, False)
                self.facing_r = False
        
        elif not self.facing_r:
            self.orig_image = pygame.transform.flip(self.orig_image, False, True)
            self.entity.image = pygame.transform.flip(self.entity.image, True, False)
            self.facing_r = True


class Gun(Weapon):
    def __init__(self, image_path, target):
        super().__init__(image_path, target)
        self.bullets = 10
        self.bullet_group = pygame.sprite.Group()

    def shoot(self):
        bullet = Bullet(("Sprites", "bullets", "bullet1.png"), (self.rect.centerx, self.rect.centery), self.target.angle_radians)
        self.bullet_group.add(bullet)

    def update(self):
        self.rotate()
        self.bullet_group.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, angle_radians):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        self.dx = 50
        self.dy = 0

        self.x = position[0] #+ self.dx * 4
        self.y = position[1] #+ self.dy * 4 
        self.angle_r = -angle_radians
        self.angle = math.degrees(angle_radians) + 90
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.time = 1.7


    def update(self):
        
        self.new_x = self.dx * math.cos(self.angle_r) - self.dy * math.sin(self.angle_r) + self.x
        self.new_y = self.dx * math.sin(self.angle_r) + self.dy * math.cos(self.angle_r) + self.y
        self.rect.centerx = self.new_x
        self.rect.centery = self.new_y
        
        wave = -math.sin(self.time) * 15
        self.time += 0.5
        self.dx += 10
        self.dy += wave


