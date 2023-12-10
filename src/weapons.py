import pygame
from settings import PX_SCALE, SHOOT_SOUND
from utils import load_image
import math
from types import FunctionType

class Weapon(pygame.sprite.Sprite):
    """
    Class representing a generic weapon in the game. This class is responsible
    for implementing the weapon rotation based on the target position.

    Parameters
    ----------
    image_path: tuple
        The path leading to the weapon image
    target_pos: tuple
        The initial position to target.
    """
    def __init__(self, image_path: tuple, target_pos: tuple):
        super().__init__()
        self._target_pos = target_pos
        self.image = load_image(image_path, 3)
        self.orig_image = self.image
        self.inventory_image = self.image
        self.rect = self.image.get_rect()
        self.facing_r = True
        self.angle_radians = 0
        self.angle_degrees = 0
        self._entity = None

    @property
    def entity(self):
        """
        The entity associated with the weapon. The weapon will orbit this entity.
        """
        return self._entity

    @entity.setter
    def entity(self, entity):
        self._entity = entity
        self.rect.center = self._entity.rect.center

    def update_target_position(self, target_pos: tuple):
        """
        Updates the position that the weapon should target.

        Parameters
        ----------
        target_pos:
            The new position to target.

        Returns
        -------
        None
        """
        self._target_pos = target_pos

    def _get_angles(self):
        self.angle_radians = math.atan2(self.entity.rect.centery-self._target_pos[1], self._target_pos[0]-self.entity.rect.centerx)
        self.angle_degrees = math.degrees(self.angle_radians)

    def _rotate(self):
        self._get_angles()
        self.image = pygame.transform.rotate(self.orig_image, self.angle_degrees)

        self.rect = self.image.get_rect(
            center = (math.cos(-self.angle_radians) * 65 + self.entity.rect.centerx,
                      math.sin(-self.angle_radians) * 80 + self.entity.rect.centery)
            )

        if -self.angle_degrees >= 90 or -self.angle_degrees <= -90:
            if self.facing_r:
                self.orig_image = pygame.transform.flip(self.orig_image, False, True)
                self.entity.image = pygame.transform.flip(self.entity.image, True, False)
                self.facing_r = False
        
        elif not self.facing_r:
            self.orig_image = pygame.transform.flip(self.orig_image, False, True)
            self.entity.image = pygame.transform.flip(self.entity.image, True, False)
            self.facing_r = True

    def update(self):
        """
        Updates the weapon. In this basic weapon, it just rotates it acordingly
        to the target.

        Returns
        -------
        None
        """
        self._rotate()

class EnemyWeapon(Weapon):
    """
    Class representing an enemy's weapon. It changes the rotation implementation
    so it doesn't flip the enemy's image.

    Parameters
    ----------
    image_path: tuple
        The path leading to the weapon image
    target_pos:
        The initial position to target.
    """
    def _rotate(self):
        self._get_angles()
        self.image = pygame.transform.rotate(self.orig_image, self.angle_degrees)

        self.rect = self.image.get_rect(
            center = (math.cos(-self.angle_radians) * 50 + self.entity.rect.centerx,
                      math.sin(-self.angle_radians) * 60 + self.entity.rect.centery)
            )

        if -self.angle_degrees >= 90 or -self.angle_degrees <= -90:
            if self.facing_r:
                self.orig_image = pygame.transform.flip(self.orig_image, False, True)
                self.entity.image = self.entity.image_right
                self.facing_r = False

        elif not self.facing_r:
            self.orig_image = pygame.transform.flip(self.orig_image, False, True)
            self.entity.image = self.entity.image_left
            self.facing_r = True

class Gun(Weapon):
    """
    Class representing a gun. A gun implements the same thing as weapons, with
    the addition of the capability of shooting. All the gun peculiaritys, like
    bullet damage and speed, are set with the dict `stats`.

    Parameters
    ----------
    image_path: tuple
        The path leading to the weapon image
    target_pos: tuple
        The initial position to target.
    stats: dict
        A dicitionary containing the gun stats.
    """
    def __init__(self, image_path, target_pos, stats):
        super().__init__(image_path, target_pos)
        self.move_function = stats["move_function"]
        self.damage = stats["damage"]
        self.mag_size = stats["mag_size"]
        self.reload_cooldown = stats["reload_cooldown"]
        self.bullet_speed = stats["bullet_speed"]
        self.bullet_sprite = stats["bullet_sprite"]

        self.bullet_group = pygame.sprite.Group()

        self.shooting = False
        self.reloading = False

        self.mag_count = self.mag_size
        self.time_empty_mag = 0
        self.time_last_reload = 0
        self.time_now = 0

    def shoot(self):
        """
        Make the gun shoot. This will create bullets and store them in the
        `bullet_group`. If the gun is in cooldown, it'll do nothing. If a shoot
        is still occuring, it'll do nothing too.

        Returns
        -------
        None
        """
        if self.shooting:
            pass
        else:
            self.shooting = True
            self._shoot()

    def _shoot(self):
        if self.mag_count > 0:
            self.shooting = True
            self.mag_count -= 1
            bullet = Bullet(
                self.bullet_sprite,
                (self.rect.centerx, self.rect.centery),
                self.angle_radians,
                self.damage,
                self.move_function,
                self.bullet_speed
            )
            self.bullet_group.add(bullet)
            if self.mag_count == 0:
                self.shooting = False
                self.time_empty_mag = self.time_now

    def _reload(self):
        self.mag_count = self.mag_size
        self.reloading = False

    def update(self):
        """
        Updates the weapon. Besides rotating the weapon, this method also will
        call tue update method to the gun active bullets.

        Returns
        -------
        None
        """
        super().update()
        self.time_now = pygame.time.get_ticks()

        if self.mag_count == 0:
            if self.time_now - self.time_empty_mag > self.reload_cooldown:
                self.reloading = True

        if self.reloading:
            self._reload()
        if self.shooting:
            self._shoot()
        self.bullet_group.update()

class EnemyGun(EnemyWeapon, Gun):
    pass

class Bullet(pygame.sprite.Sprite):
    """
    Class representing a bullet. The class is the same for enemies and the
    player. The bullets needs some parameters, including the trajectory function,
    to determine damages and such. What should be used to diferentiate from
    where the bullet comes from is the group it is contained.

    Parameters
    ----------
    image_path: tuple
        The path to the bullet image.
    position: tuple
        The initial position of the bullet.
    angle_radians: float
        The angle that the bullet is being shoot.
    damage: int
        The damage the bullet should.
    move_function: function
        A function to determine the bullet trajectory. This function should take
        one variable (the time elapsed since the bullet was shoot) and should
        return only a float or int.
    speed: int
        The speed of the bullet
    """
    def __init__(self, image_path: tuple, position: tuple, angle_radians: float, damage: int, move_function: FunctionType, speed: int):
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
        self.image = pygame.transform.rotate(
            self.orig_image,
            math.degrees(angle_radians)
        )
        self.travel_time = 0
        self.function = move_function
        self.speed = speed

    def update(self):
        """
        Updates the bullet. This will make it go futher, acordingly to the
        trajectory function passed. This ins't made for being called alone, but
        to be called when the bullet group is being updated.

        Returns
        -------
        None
        """
        self.new_x = self.dx * math.cos(self.angle_r) - self.dy * math.sin(self.angle_r) + self.x
        self.new_y = self.dx * math.sin(self.angle_r) + self.dy * math.cos(self.angle_r) + self.y
        self.rect.centerx = self.new_x
        self.rect.centery = self.new_y
        
        wave = self.function(self.travel_time)
        self.travel_time += 0.5
        self.dx += self.speed
        self.dy += wave

        if self.travel_time > 100:
            self.kill()
