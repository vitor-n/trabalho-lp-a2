import pygame as pg
from settings import PX_SCALE
from utils import load_image


class Health:
    def __init__(self, image_path, max_health):
        self.image = load_image(image_path, PX_SCALE)
        self.rect = self.image.get_rect()
        self.max_health = max_health
        self.current_health = max_health

        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()


    def decrease(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def increase(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def get_health(self):
        return self.current_health

    def draw(self, surface, x,y):
        health_bar_width = (self.current_health / self.max_health) * self.image_width
        health_bar_rect = pg.Rect(x+1, y+1, health_bar_width-2, self.image_height-4)
        pg.draw.rect(surface, "#F50104", health_bar_rect)
        surface.blit(self.image, (x, y))
        
