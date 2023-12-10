import pygame as pg
from player import Entity
import settings as st
from settings import SCREEN_DIMENSIONS
import random

class Enemy(Entity):

    def __init__(self, image_path, target_position, speed, life):
        super().__init__(image_path, self.initial_position(target_position))
        self.speed = speed
        self.life = life

    def move(self, delta_time):
        self.direction.normalize_ip()
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time
    
    def initial_position(self, target_position):
        pos_x = random.randint(target_position[0] - SCREEN_DIMENSIONS[0]/2, target_position[0] + SCREEN_DIMENSIONS[0]/2)
        pos_y = random.randint(target_position[1] - SCREEN_DIMENSIONS[1]/2, target_position[1] + SCREEN_DIMENSIONS[1]/2)
        pos = (pos_x, pos_y)
        return pos
     
    def define_direction(self, player_position):
        delta_x = player_position.x - self.rect.x
        delta_y = player_position.y - self.rect.y

        delta_pos = pg.Vector2(delta_x, delta_y)
        mag = delta_pos.magnitude_squared()
        if mag != 0:
            delta_pos.normalize_ip()
        return (delta_pos, mag)
    
    def update(self, player_position, delta_time, integral_gang):
        (self.direction, _) = self.define_direction(player_position)
        self.remove_overlapping(integral_gang)
        if self.direction.magnitude_squared() != 0:
            self.move(delta_time)
    
    def remove_overlapping(self, integral_gang): #list containing all Sprites in a Group that intersect with another Sprite
        collide_list = pg.sprite.spritecollide(self, integral_gang, dokill = False)
        for sprite in collide_list:
            if sprite == self:
                continue
            (delta_pos, mag) = self.define_direction(sprite.rect)
            self.direction -= delta_pos * 2
        
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
    
  


