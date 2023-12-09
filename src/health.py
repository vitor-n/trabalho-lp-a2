import pygame as pg
from utils import load_image

class Health:
    def __init__(self, max_health):
        self._max_health = max_health
        self._current_health = max_health

    def decrease(self, amount):
        self._current_health -= amount
        if self._current_health < 0:
            self._current_health = 0

    def increase(self, amount):
        self._current_health += amount
        if self._current_health > self._max_health:
            self._current_health = self._max_health

    def get_health(self):
        return self._current_health
    
    def __eq__(self, num):
        return num == self._current_health

    def __sub__(self, num):
        return Health(self.decrease(num))
    
    def __add__(self, num):
        return Health(self.increase(num))

    
class PlayerHealth(Health):
    def __init__(self, max_health):
        super().__init__(max_health)
        self._image_full_heart = load_image(("Sprites", "healthbar", "player_full_heart.png"))
        self._image_half_heart = load_image(("Sprites", "healthbar", "player_half_heart.png"))
        self._rect = self._image_full_heart.get_rect()
        
        self._full_hearts = self._current_health // 2
        self._half_hearts = self._current_health % 2
        
        self.bar = pg.Surface((self._rect.width * (self._full_hearts + self._half_hearts), self._rect.height))
        self.bar.set_colorkey((255,0,255))

    def update(self):
        self._full_hearts = int(self._current_health // 2)
        self._half_heart = int(self._current_health % 2)

        self.bar.fill((255,0,255))
        for i in range(self._full_hearts):
            self.bar.blit(self._image_full_heart, (i * self._rect.width, 0))

        if self._half_heart:
            self.bar.blit(self._image_half_heart, (self._full_hearts * self._rect.width, 0))
        