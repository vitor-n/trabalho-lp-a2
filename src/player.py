import pygame as pg
from settings import PX_SCALE, DASH_SOUND
from utils import load_image
from health import PlayerHealth
from weapons import Weapon

class Entity(pg.sprite.Sprite):
    """
    Generic class to represent any entity. An entity is something that have a
    sprite and can move within the map.

    Parameters
    ----------
    image_path: tuple
        A tuple containing the directory names leading to the entity image.
    initial_position: tuple
        The position where the entity should be when created. Defaults to (0, 0).
    """
    def __init__(self, image_path: tuple, initial_position: tuple = (0, 0)):
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
    image_path: tuple
        A tuple containing the directory names leading to the player image.
    initial_position: tuple
        The position where the entity should be when created. Defaults to (0, 0).
    inventory: Inventory
        A inventory to hold the player guns.
    """
    def __init__(self, image_path: tuple , initial_position: tuple, inventory):
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

    @property
    def weapon(self):
        """
        The weapon being held by the player. This is not changeable, and to
        swap weapons the inventory should be used instead.
        """
        return self.inventory.weapon

    def update(self, target_pos: tuple):
        """
        Updates the player. This will move if inputed to, will check if the gun
        needs to be changed and will call update for the gun.

        Parameters
        ----------
        target_pos: tuple
            the coordinates of where the player gun should aim.

        Returns
        -------
        None
        """
        self._get_input()

        if self.direction.magnitude_squared() != 0:
           self._move(self.speed)

        if self.weapon:
            self.weapon.update_target_position(target_pos)
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

    def _get_input(self):
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
            DASH_SOUND.play()

        if len(self.inventory) > 1:
            for mouse_event in pg.event.get(pg.MOUSEWHEEL):
                if not self.weapon.shooting:
                    if mouse_event.y > 0:
                        self.inventory.next_weapon()
                    elif mouse_event.y < 0:
                        self.inventory.previous_weapon()
                    if keys[pg.K_r]:
                        self.inventory.next_weapon()
                    elif keys[pg.K_t]:
                        self.inventory.previous_weapon


        if pg.mouse.get_pressed()[0]:
            self.attacking = True
        else:
            self.attacking = False

    def _move(self, speed):
        self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

class Inventory:
    """
    Class representing a inventory. It is responsible for holding guns,
    their names and their position in a queue. It also implements methods
    to swtich to the next or previous gun.
    """
    def __init__(self):
        self._weapons = []
        self._current_weapon = 0
        self._player = None

    def __len__(self):
        return len(self._weapons)

    @property
    def player(self):
        """
        The player associated with the inventory.
        """
        return self._player

    @player.setter
    def player(self, player):
        self._player = player

    @property
    def weapon(self):
        """
        The current weapon selected in the inventory. If the inventory is empty,
        returns None. To change weapon, use `next_weapon` and `previous_weapon`.
        """
        if len(self._weapons):
            return self._weapons[self._current_weapon]["weapon"]

    def add_weapon(self, weapon: Weapon, name: str):
        """
        Adds a weapon to the inventory. If the weapon is already added, does
        nothing.

        Parameters
        ----------
        weapon:
            The weapon to be added to the inventory.
        name:
            The name to be displayed for the weapon.

        Returns
        -------
        None
        """
        for existing_weapon in self._weapons:
            if existing_weapon["weapon"] == weapon:
                break
        else:
            self._weapons.append(
                {"weapon": weapon,
                 "name": name}
            )
            weapon.entity = self.player

    def remove_weapon(self, weapon: Weapon):
        """
        Removes a weapon from the inventory. If it isn't added, does nothing.

        Parameters
        ----------
        weapon:
            The weapon to be removed of the inventory.

        Returns
        -------
        None
        """
        for existing_weapon in self._weapons.copy():
            if existing_weapon["weapon"] == weapon:
                self._weapons.remove(existing_weapon)
                return

    def next_weapon(self):
        """
        Changes the weapon to the next in the queue. If it's the last, changes
        to the first one.

        Returns
        -------
        None
        """
        self._current_weapon += 1
        if self._current_weapon == len(self._weapons):
            self._current_weapon = 0

    def previous_weapon(self):
        """
        Changes the weapon to the previous in the queue. If it's the first,
        changes to the last one.

        Returns
        -------
        None
        """
        self._current_weapon -= 1
        if self._current_weapon == -1:
            self._current_weapon = len(self._weapons) - 1

    def update(self):
        """
        Updates the selected gun and it's bullets. For the other guns that are
        not selected, updates only their bullets.

        Returns
        -------
        None
        """
        for weapon in self._weapons:
            if hasattr(weapon["weapon"], "bullet_group") and weapon["weapon"] != self.weapon:
                weapon["weapon"].bullet_group.update()
        if self.weapon:
            self.weapon.update()

    def get_current_weapon_names(self):
        """
        Returns the names of the selected, previous and next gun. This turns
        possible bliting in the screen the names, so the player can know the
        current gun and the switch options.

        Returns
        -------
        tuple: An tuple with the previous, selected and next guns names, respectivelly.
        """
        previous = self._weapons[self._current_weapon - 1]["name"]
        current = self._weapons[self._current_weapon]["name"]
        if self._current_weapon == len(self._weapons) - 1:
            next_ = self._weapons[0]["name"]
        else:
            next_ = self._weapons[self._current_weapon + 1]["name"]
        return previous, current, next_
