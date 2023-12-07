import pygame as pg
from player import Entity
import settings as st

class Enemy(Entity):

    def __init__(self, image_path, initial_position, speed, life):
        super().__init__(image_path, initial_position)
        self.speed = speed
        self.life = life

    def move(self, delta_time):
        self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed * delta_time
        self.rect.y += self.direction.y * self.speed * delta_time

    def define_direction(self, player_position):
        delta_x = player_position.x - self.rect.x
        delta_y = player_position.y - self.rect.y

        self.direction = pg.Vector2(delta_x, delta_y)
    
    def update(self, player_position, delta_time):
        self.define_direction(player_position)
        if self.direction.magnitude_squared() != 0:
            self.move(delta_time)
        

class Apache(Enemy):
    def __init__(self, initial_position, integral_type):
        speed = st.APACHE_SPEED[integral_type - 1]
        life = st.APACHE_HEALTH[integral_type - 1]
        image_path = st.INTEGRALS_SPRITES.copy()
        image_path.append(st.APACHE_IMAGE[integral_type - 1])
        super().__init__(image_path, initial_position, speed, life)
        

class Roman(Enemy):
    def __init__(self, initial_position, integral_type):
        speed = st.ROMAN_SPEED[integral_type - 1]
        life = st.ROMAN_HEALTH[integral_type - 1]
        image_path = st.INTEGRALS_SPRITES.copy().append(st.ROMAN_IMAGE[integral_type - 1])
        super().__init__(image_path, initial_position, speed, life)

class Samurai(Enemy):
    def __init__(self, initial_position, integral_type):
        speed = st.SAMURAI_SPEED[integral_type - 1]
        life = st.SAMURAI_HEALTH[integral_type - 1]
        image_path = st.INTEGRALS_SPRITES.copy().append(st.SAMURAI_IMAGE[integral_type - 1])
        super().__init__(image_path, initial_position, speed, life)

class Viking(Enemy): 
    def __init__(self, initial_position, integral_type):
        speed = st.VIKING_SPEED[integral_type-1]
        life = st.VIKING_HEALTH[integral_type - 1]
        image_path = st.INTEGRALS_SPRITES.copy().append(st.VIKING_IMAGE[integral_type - 1])
        super().__init__(image_path, initial_position, speed, life)
        