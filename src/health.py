import pygame as pg
from utils import load_image
from settings import HIT_SOUND

class Health:
    """
    Class that represents the health of an entity.

    """
    def __init__(self, max_health, immunity_time=0):
        self._max_health = max_health
        self._current_health = max_health
        self._immunity_time = immunity_time
        self._last_hit = 0

    def decrease(self, amount: int | float):
        """
        Decreases the current health by the specified amount, taking into account immunity time.
        
        Parameters
        ----------
        amount: int or float
            The amount to decrease the health by.
        """
        time_now = pg.time.get_ticks() / 1000
        if (time_now - self._last_hit) > self._immunity_time:
            self._current_health -= amount
            if self._current_health < 0:
                self._current_health = 0
            self._last_hit = time_now

    def increase(self, amount: int | float):
        """
        Increases the current health by the specified amount.
        
        Parameters
        ----------
        amount: int or float
            The amount to decrease the health by.
        """
        self._current_health += amount
        if self._current_health > self._max_health:
            self._current_health = self._max_health

    def get_health(self):
        """
        Returns the current health value.
        
        Returns
        -------
        int 
            The current health value.
        """
        return self._current_health
    
    def __eq__(self, num):
        """
        Checks if the current health is equal to the specified number.
        
        Parameters
        ----------
        num: int
            The number to compare with the current health.
        
        Returns
        -------
        bool
            True if the current health is equal to the specified number, False otherwise.
        """
        return num == self._current_health

    def __sub__(self, num):
        """
        Decreases the current health by the specified number
        
        Parameters
        ----------
        num: int
            The number to decrease the health by.
    
        Returns
        -------
        Health:
            The Health object instance with the updated health value.
        """
        return self.decrease(num)
    
    def __add__(self, num):
        """
        Increases the current health by the specified number and returns a new Health object.
        
        Parameters
        ----------
        num: int
          The number to increase the health by.
        
        Returns
        -------
        Health:
            The Health object instance with the updated health value.
        """
        return self.increase(num)

    
class PlayerHealth(Health):
    """
    Class that represents the health of the player.
    """
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
        """
        Decreases the player's health by the specified amount.
        
        Parameters
        ----------
        amount: int)
            The amount to decrease the health by.
        """
        time_now = pg.time.get_ticks() / 1000
        if (time_now - self._last_hit) > self._immunity_time:
            self._current_health -= amount
            if self._current_health < 0:
                self._current_health = 0
            self._last_hit = time_now
            HIT_SOUND.play()
            
    def update(self):
        """
        Updates the health bar based on the current health.
        """
        self._full_hearts = int(self._current_health // 2)
        self._half_heart = int(self._current_health % 2)

        self.bar.fill((255,0,255))
        for i in range(self._full_hearts):
            self.bar.blit(self._image_full_heart, (i * self._rect.width, 0))

        if self._half_heart:
            self.bar.blit(self._image_half_heart, (self._full_hearts * self._rect.width, 0))
        