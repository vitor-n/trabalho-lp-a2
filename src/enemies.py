from typing import Iterable, Union
import pygame as pg
from pygame.sprite import AbstractGroup
from player import Entity
import settings as st
from settings import SCREEN_DIMENSIONS
import random
from health import Health

class Enemy(Entity):

    def __init__(self, image_path, target_position, speed, health, target = None):
        super().__init__(image_path, self.initial_position(target_position))
        self.speed = speed
        self.health = Health(health, 0)
        self._target = target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

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

        if self.health == 0:
            self.kill
    
    
class Apache(Enemy):
    def __init__(self, target_position, integral_type):
        speed = st.integrals_info['APACHE_SPEED'][integral_type - 1]
        life = st.integrals_info['APACHE_HEALTH'][integral_type - 1]
        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['APACHE_IMAGE'][integral_type - 1])
        super().__init__(image_path, target_position, speed, life)
        
class Roman(Enemy):
    def __init__(self, target_position, integral_type):
        speed = st.integrals_info['ROMAN_SPEED'][integral_type - 1]
        life = st.integrals_info['ROMAN_HEALTH'][integral_type - 1]
        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['ROMAN_IMAGE'][integral_type - 1])
        super().__init__(image_path, target_position, speed, life)

class Samurai(Enemy):
    def __init__(self, target_position, integral_type):
        speed = st.integrals_info['SAMURAI_SPEED'][integral_type - 1]
        life = st.integrals_info['SAMURAI_HEALTH'][integral_type - 1]
        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['SAMURAI_IMAGE'][integral_type - 1])
        super().__init__(image_path, target_position, speed, life)

class Viking(Enemy): 
    def __init__(self, target_position, integral_type):
        speed = st.integrals_info['VIKING_SPEED'][integral_type-1]
        life = st.integrals_info['VIKING_HEALTH'][integral_type - 1]
        image_path = st.integrals_info['INTEGRALS_SPRITES'].copy()
        image_path.append(st.integrals_info['VIKING_IMAGE'][integral_type - 1])
        super().__init__(image_path, target_position, speed, life)

class IntegralGang(pg.sprite.Group):


    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.types = [Apache, Roman, Samurai, Viking]

    def create_group(self, integral_family,single_qtt, double_qtt, triple_qtt, target_position):
        
        for num in range(single_qtt):
            enemy_s = integral_family((target_position), 1)
            self.add(enemy_s)
        for num in range(double_qtt):
            enemy_d = integral_family((target_position), 2)
            self.add(enemy_d)
        for num in range(triple_qtt):
            enemy_t = integral_family((target_position), 3)
            self.add(enemy_t)

    def random_group(self,single_qtt, double_qtt, triple_qtt, target_position):
        
        self.create_group(self.types[random.randint(0,3)], single_qtt, double_qtt, triple_qtt, target_position)
    
    def set_target(self, target):
        for integral in self:
            integral.target = target
        


