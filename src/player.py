import pygame as pg
from settings import PX_SCALE
from utils import load_image

class Entity(pg.sprite.Sprite):
    """
    Generic class to represent any entity. An entity is something that have a
    sprite and can move within the map.

    Parameters
    ----------
    image_path:
        A tuple containing the directory names leading to the entity image.
    initial_position:
        The position where the entity should be when created. Defaults to (0, 0).
    """
    def __init__(self, image_path, initial_position = (0, 0)):
        super().__init__()
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(center = initial_position)
        self.direction = pg.math.Vector2()

class Player(Entity):
    """
    Class representing the player. It implements some functions that are used
    to move the player based on keyboard inputs.

    Parameters
    ----------
    image_path:
        A tuple containing the directory names leading to the player image.
    initial_position:
        The position where the entity should be when created. Defaults to (0, 0).
    map_size:
        The map size. It is used to determine when the player is on the map edge.
    """

    def __init__(self, image_path, initial_position, weapon = None):
        super().__init__(image_path, initial_position)
        self.speed = 7
        
        self.weapon = weapon
        self.attacking = False

        self.dashing = False
        self.last_dash = 0
        self.dash_cooldown = 2000
        self.dash_duration = 10
        self.dash_timer = self.dash_duration

    def set_weapon(self, weapon):
        self.weapon = weapon
        weapon.set_entity(self)

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w] and not keys[pg.K_s]:
            self.direction.y = -1
        elif keys[pg.K_s] and not keys[pg.K_w]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pg.K_d] and not keys[pg.K_a]:
            self.direction.x = 1
        elif keys[pg.K_a] and not keys[pg.K_d]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pg.K_SPACE] and (pg.time.get_ticks() - self.last_dash) > self.dash_cooldown:
            self.dashing = True
            self.last_dash = pg.time.get_ticks()

        if self.weapon:
            for event in pg.event.get():
                if event.type == pg.MOUSEWHEEL:
                    self.weapon.bullet_type = event.y

        if pg.mouse.get_pressed()[0]:
            self.attacking = True
        else:
            self.attacking = False

    def move(self, speed):
        self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed
    
    def update(self):
        
        self.get_input()

        if self.direction.magnitude_squared() != 0:
           self.move(self.speed)

        if self.weapon:
            if self.attacking:
                self.weapon.shoot()
            self.weapon.update()

        if self.dashing:
            self.speed = 20
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
                self.speed = 7
                self.dash_timer = self.dash_duration