from typing import Iterable, Union
import pygame as pg
from pygame.sprite import AbstractGroup
from player import Entity
import settings as st
from settings import SCREEN_DIMENSIONS
import random
from health import Health
from weapons import EnemyWeapon
from utils import load_image

zero_gun_stats = {
    "move_function": lambda m: 0,
    "damage": 10,
    "mag_size": 1,
    "reload_cooldown": 3000,
    "bullet_speed": 10,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

class Enemy(Entity):

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
        self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time
    
    def initial_position(self, target_position):
        pos_x = random.randint(target_position[0] - SCREEN_DIMENSIONS[0]/2, target_position[0] + SCREEN_DIMENSIONS[0]/2)
        pos_y = random.randint(target_position[1] - SCREEN_DIMENSIONS[1]/2, target_position[1] + SCREEN_DIMENSIONS[1]/2)
        pos = (pos_x, pos_y)
        return pos
     
    def define_direction(self):
        delta_x = self.target.rect.x - self.rect.x
        delta_y = self.target.rect.y - self.rect.y
        self.direction = pg.Vector2(delta_x, delta_y)
    
    def update(self, delta_time):
        self.define_direction()
        if self.direction.magnitude_squared() != 0:
            self.move(delta_time)

        if self.weapon:
            self.weapon.set_target(self.target.rect.topleft)
            self.weapon.update()

        if self.health == 0:
            self.kill
    
    
class Apache(Enemy):
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['APACHE_SPEED'][integral_type - 1]
        life = st.integrals_info['APACHE_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['APACHE_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["APACHE_WEAPONS"][integral_type - 1])
        weapon = EnemyWeapon(weapon_path, target)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class Roman(Enemy):
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
    def __init__(self, target_position, integral_type, target):
        speed = st.integrals_info['SAMURAI_SPEED'][integral_type - 1]
        life = st.integrals_info['SAMURAI_HEALTH'][integral_type - 1]

        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['SAMURAI_IMAGE'][integral_type - 1])

        weapon_path = st.integrals_info["INTEGRALS_WEAPONS"].copy()
        weapon_path.append(st.integrals_info["SAMURAI_WEAPONS"][integral_type - 1])
        weapon = EnemyWeapon(weapon_path, target)

        super().__init__(image_path, target_position, speed, life, target, weapon)

class Viking(Enemy): 
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
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.types = [Apache, Roman, Samurai, Viking]

    def create_group(self, integral_family, single_qtt, double_qtt, triple_qtt, target_position, target = None):
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
        self.create_group(self.types[random.randint(0,3)], single_qtt, double_qtt, triple_qtt, target_position, target)
    
    def set_target_for_all(self, target):
        for integral in self:
            integral.target = target
        


