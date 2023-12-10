import pygame as pg
from utils import load_image
from settings import HIT_SOUND

class Health:
    def __init__(self, max_health, immunity_time=0):
        self._max_health = max_health
        self._current_health = max_health
        self._immunity_time = immunity_time
        self._last_hit = 0

    def decrease(self, amount):
        time_now = pg.time.get_ticks() / 1000
        if (time_now - self._last_hit) > self._immunity_time:
            self._current_health -= amount
            if self._current_health < 0:
                self._current_health = 0
            self._last_hit = time_now

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
    def __init__(self, max_health, immunity_time=0):
        super().__init__(max_health, immunity_time)
        self._image_full_heart = load_image(("Sprites", "healthbar", "player_full_heart.png"))
        self._image_half_heart = load_image(("Sprites", "healthbar", "player_half_heart.png"))
        self._rect = self._image_full_heart.get_rect()
        
        self._full_hearts = self._current_health // 2
        self._half_hearts = self._current_health % 2
        
        self.bar = pg.Surface((self._rect.width * (self._full_hearts + self._half_hearts), self._rect.height))
        self.bar.set_colorkey((255,0,255))

    def decrease(self, amount):
        time_now = pg.time.get_ticks() / 1000
        if (time_now - self._last_hit) > self._immunity_time:
            self._current_health -= amount
            if self._current_health < 0:
                self._current_health = 0
            self._last_hit = time_now
            HIT_SOUND.play()
            

    def update(self):
        self._full_hearts = int(self._current_health // 2)
        self._half_heart = int(self._current_health % 2)

        self.bar.fill((255,0,255))
        for i in range(self._full_hearts):
            self.bar.blit(self._image_full_heart, (i * self._rect.width, 0))

        if self._half_heart:
            self.bar.blit(self._image_half_heart, (self._full_hearts * self._rect.width, 0))
        