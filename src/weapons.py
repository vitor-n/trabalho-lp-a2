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
        self.move_function = lambda m: 0
        self.damage = 5
        self.mag_size = 1
        self.reload_cooldown = 500
        self.bullet_speed = 10


        self.bullet_group = pygame.sprite.Group()

        self.shooting = False
        self.reloading = False

        self.mag_count = self.mag_size
        self.time_empty_mag = 0
        self.time_last_reload = 0
        self.time_now = 0


    def shoot(self):
        if self.mag_count > 0:
            self.shooting = True
            self.mag_count -= 1
            bullet = Bullet(("Sprites", "bullets", "bullet1.png"), (self.rect.centerx, self.rect.centery), self.target.angle_radians, self.damage, self.move_function, self.bullet_speed)
            self.bullet_group.add(bullet)
            if self.mag_count == 0:
                self.shooting = False
                self.time_empty_mag = self.time_now

    def reload(self):
        self.mag_count = self.mag_size
        self.reloading = False

    def update(self):
        self.time_now = pygame.time.get_ticks()

        if self.mag_count == 0:
            if self.time_now - self.time_empty_mag > self.reload_cooldown:
                self.reloading = True

        if self.reloading:
            self.reload()
        if self.shooting:
            self.shoot()
        if self.reloading:
            self.reload()
        self.rotate()
        self.bullet_group.update()

class SineShotgun(Gun):
    def __init__(self, image_path, target):
        super().__init__(image_path, target)
        self.mag_size = 30
        self.mag_count = self.mag_size
        self.reload_cooldown = 1000
        self.bullet_speed = 20

        def move_function(time):
            return math.cos(time) * 40
        self.move_function = move_function
        self.damage = 2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, position, angle_radians, damage, move_function, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.damage = damage
        self.dx = 50
        self.dy = 0
        self.x = position[0]
        self.y = position[1]
        self.angle_r = -angle_radians
        self.angle = math.degrees(angle_radians) + 90
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.travel_time = 0
        self.function = move_function
        self.speed = speed


    def update(self):
        def function(gun):
            return math.sin(gun) * 40
        self.new_x = self.dx * math.cos(self.angle_r) - self.dy * math.sin(self.angle_r) + self.x
        self.new_y = self.dx * math.sin(self.angle_r) + self.dy * math.cos(self.angle_r) + self.y
        self.rect.centerx = self.new_x
        self.rect.centery = self.new_y
        
        wave = self.function(self.travel_time)
        self.travel_time += 0.5
        self.dx += self.speed
        self.dy += wave


