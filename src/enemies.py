import pygame as pg
from player import Entity
import settings as st
from settings import SCREEN_DIMENSIONS
import random
from health import Health
from weapons import EnemyWeapon, EnemyGun
from utils import load_image

class Enemy(Entity):
    """Class with methods for a generic enemy.

    Parameters
    ----------
    image_path : A tuple containing the directory name leading to the entity image.

    target_position: A tuple indicating the position of the player or another target.

    speed: The speed of the enemy.

    health: The maximum health of the enemy.
    """

    def __init__(self, image_path, target_position, speed, health, target = None, weapon = None):
        super().__init__(image_path, self.initial_position(target_position))
        self.image_left = self.image
        image_path[-1] = image_path[-1].replace(".png", "_left.png")
        self.image_right = load_image(image_path)
        self.speed = speed
        self.health = Health(health, 0)
        self._target = target
        self._weapon = weapon
        if weapon:
            self._weapon.set_entity(self)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def weapon(self):
        return self._weapon

    def move(self, delta_time):
        """Function to move the enemy.

        Parameters
        ----------
        delta_time : Time between frames. Used for calculating displacement.
        """
        self.direction.normalize_ip()
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time
    
    def initial_position(self, target_position):
        """Creates a random position to spawn an enemy.

        Parameters
        ----------
        target_position : A tuple indicating the position of the player or another target.

        Returns
        -------
        Tuple containing the random position.
        """
        pos_x = random.randint(target_position[0] - SCREEN_DIMENSIONS[0]/2, target_position[0] + SCREEN_DIMENSIONS[0]/2)
        pos_y = random.randint(target_position[1] - SCREEN_DIMENSIONS[1]/2, target_position[1] + SCREEN_DIMENSIONS[1]/2)
        pos = (pos_x, pos_y)
        return pos
     
    def define_direction(self, player_position):
        """
        Creates a tuple that holds the displacement beetween player and an enemy and its magnetude.

        Parameters
        ----------
        player_position : A tuple indicating the position of the player.

        Returns
        -------
        Tuple holding values.
        """
        delta_x = player_position.x - self.rect.x
        delta_y = player_position.y - self.rect.y

        delta_pos = pg.Vector2(delta_x, delta_y)
        mag = delta_pos.magnitude_squared()
        if mag != 0:
            delta_pos.normalize_ip()
        return (delta_pos, mag)
    
    def update(self, delta_time, integral_gang):
        """
        Method that updates the enemy movements inside the loop game.

        Parameters
        ----------
        delta_time : Time between frames. 

        integral_gang : Object of type IntegralGang. Represents a group of warrior integrals of the same kind.
        """
        (self.direction, _) = self.define_direction(self.target.rect)
        self.remove_overlapping(integral_gang)

        if self.direction.magnitude_squared() != 0:
            self.move(delta_time)

        if self.weapon:
            self.weapon.set_target(self.target.rect.topleft)
            self.weapon.update()
            if type(self.weapon) == EnemyGun:
                self.weapon.shoot()

        if self.health == 0:
            self.kill
    
    def remove_overlapping(self, integral_gang): 
        """
        Make enemies reppel themselves to minimize the overlapping .
        Parameters
        ----------
        integral_gang : Object of type IntegralGang. Represents a group of warrior integrals of the same kind.
        """
        collide_list = pg.sprite.spritecollide(self, integral_gang, dokill = False)
        for sprite in collide_list:
            if sprite == self:
                continue
            (delta_pos, mag) = self.define_direction(sprite.rect)
            self.direction -= delta_pos * 2
        
class Apache(Enemy):
    """
    Class that creates an object representing an apache warrior integral. 

    Parameters
    ----------
    target_position: A tuple indicating the position of the player or another target.

    integral_type: Integer to indicate a single, double or triple integral.
    """
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['APACHE_SPEED'][integral_type - 1]
        life = st.integrals_info['APACHE_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['APACHE_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["APACHE_WEAPONS"][integral_type - 1])
        weapon_stats = st.integrals_info["APACHE_GUNS"][integral_type - 1]
        weapon_stats["move_function"] = lambda m: 0
        weapon = EnemyGun(weapon_path, target, weapon_stats)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class Roman(Enemy):
    """
    Class that creates an object representing a roman warrior integral.

    Parameters
    ----------
    target_position: A tuple indicating the position of the player or another target.

    integral_type: Integer to indicate a single, double or triple integral.
    """
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['ROMAN_SPEED'][integral_type - 1]
        life = st.integrals_info['ROMAN_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['ROMAN_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["ROMAN_WEAPONS"][integral_type - 1])
        weapon = EnemyWeapon(weapon_path, target)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class Samurai(Enemy):
    """
    Class that creates an object representing a samurai warrior integral.

    Parameters
    ----------
    target_position: A tuple indicating the position of the player or another target.

    integral_type: Integer to indicate a single, double or triple integral.
    """
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['SAMURAI_SPEED'][integral_type - 1]
        life = st.integrals_info['SAMURAI_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['SAMURAI_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["SAMURAI_WEAPONS"][integral_type - 1])
        if integral_type == 3:
            weapon_stats = st.integrals_info["SAMURAI_LANCE"]
            weapon_stats["move_function"] = lambda m: 0
            weapon = EnemyGun(weapon_path, target, weapon_stats)
        else:
            weapon = EnemyWeapon(weapon_path, target)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class Viking(Enemy): 
    """
    Class that creates an object representing a viking warrior integral.

    Parameters
    ----------
    target_position: A tuple indicating the position of the player or another target.

    integral_type: Integer to indicate a single, double or triple integral.
    """
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['VIKING_SPEED'][integral_type-1]
        life = st.integrals_info['VIKING_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['VIKING_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["VIKING_WEAPONS"][integral_type - 1])
        weapon = EnemyWeapon(weapon_path, target)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class IntegralGang(pg.sprite.Group):
    """
    Class representing a group of integrals to be spawned on the loop game. 

    Parameters
    ----------
    *sprites: The group of enemies to create a gang or to be added to an existing one.
    """

    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.types = [Apache, Roman, Samurai, Viking]

    def create_group(self, integral_family,single_qtt, double_qtt, triple_qtt, target_position, target = None):
        """
        Creates a group of integrals of a choosen warrior type.

        Parameters
        ----------
        integral_family : The class name of the warrior type.

        single_qtt : Number of single integrals of the choosen type to be added.
        _
        double_qtt : Number of double integrals of the choosen type to be added.

        triple_qtt : Number of triple integrals of the choosen type to be added.

        target_position : A tuple indicating the position of the player or another target.

        """
        
        for num in range(single_qtt):
            enemy_s = integral_family((target_position), 1, target)
            self.add(enemy_s)
        for num in range(double_qtt):
            enemy_d = integral_family((target_position), 2, target)
            self.add(enemy_d)
        for num in range(triple_qtt):
            enemy_t = integral_family((target_position), 3, target)
            self.add(enemy_t)

    def random_group(self,single_qtt, double_qtt, triple_qtt, target_position, target = None):
        """
        Creates a group of a random warrior type. Similar to create_group. 

        Parameters
        ----------
        integral_family : The class name of the warrior type.

        single_qtt : Number of single integrals of the choosen type to be added.
        _
        double_qtt : Number of double integrals of the choosen type to be added.

        triple_qtt : Number of triple integrals of the choosen type to be added.

        target_position : A tuple indicating the position of the player or another target.
        """
        self.create_group(self.types[random.randint(0,3)], single_qtt, double_qtt, triple_qtt, target_position, target)

    def set_target_for_all(self, target):
        for integral in self:
            integral.target = target
        


