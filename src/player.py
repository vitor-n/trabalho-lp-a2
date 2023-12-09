import pygame as pg
from settings import PX_SCALE
from utils import load_image
from health import Health, PlayerHealth

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

    def __init__(self, image_path, initial_position, inventory):
        super().__init__(image_path, initial_position)
        self.health = PlayerHealth(6, 2)
        self.speed = 7
        
        self.inventory = inventory
        self.inventory.player = self
        self.attacking = False

        self.dashing = False
        self.last_dash = 0
        self.dash_cooldown = 2000
        self.dash_duration = 10
        self.dash_timer = self.dash_duration
        self.coords = (self.rect.centerx, self.rect.centery)

    #def set_weapon(self, weapon):
    #    self.weapon = weapon
    #    weapon.set_entity(self)

    @property
    def weapon(self):
        return self.inventory.weapon

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

        if len(self.inventory) > 1:
            if not self.weapon.shooting:
                if keys[pg.K_r]:
                    self.inventory.next_weapon()
                elif keys[pg.K_t]:
                    self.inventory.previous_weapon

        #if self.weapon:
        #    for event in pg.event.get():
        #        if event.type == pg.MOUSEWHEEL:
        #            self.weapon.bullet_type = event.y

        if pg.mouse.get_pressed()[0]:
            self.attacking = True
        else:
            self.attacking = False

    def move(self, speed):
        self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed
    
    def update(self, target_pos):
        
        self.get_input()

        if self.direction.magnitude_squared() != 0:
           self.move(self.speed)

        if self.weapon:
            self.weapon.target_pos = target_pos
            if self.attacking:
                self.weapon.shoot()
        self.inventory.update()

        if self.dashing:
            self.speed = 20
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
                self.speed = 7
                self.dash_timer = self.dash_duration

        self.health.update()

class Inventory:
    def __init__(self):
        self._weapons = []
        self._current_weapon = 0
        self._player = None

    def __len__(self):
        return len(self._weapons)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player

    @property
    def weapon(self):
        if len(self._weapons):
            return self._weapons[self._current_weapon]["weapon"]

    def add_weapon(self, weapon, name):
        for existing_weapon in self._weapons:
            if existing_weapon["weapon"] == weapon:
                break
        else:
            self._weapons.append(
                {"weapon": weapon,
                 "name": name}
            )
            weapon.set_entity(self.player)

    def remove_weapon(self, weapon):
        for existing_weapon in self._weapons.copy():
            if existing_weapon["weapon"] == weapon:
                self._weapons.remove(existing_weapon)


    def next_weapon(self):
        self._current_weapon += 1
        if self._current_weapon == len(self._weapons):
            self._current_weapon = 0

    def previous_weapon(self):
        self._current_weapon -= 1
        if self._current_weapon == -1:
            self._current_weapon = len(self._weapons) - 1

    def update(self):
        for weapon in self._weapons:
            if hasattr(weapon["weapon"], "bullet_group") and weapon["weapon"] != self.weapon:
                weapon["weapon"].bullet_group.update()
        if self.weapon:
            self.weapon.update()

    def get_current_weapon_names(self):
        previous = self._weapons[self._current_weapon - 1]["name"]
        current = self._weapons[self._current_weapon]["name"]
        if self._current_weapon == len(self._weapons) - 1:
            next_ = self._weapons[0]["name"]
        else:
            next_ = self._weapons[self._current_weapon + 1]["name"]
        return previous, current, next_
