import pygame as pg

class Health:
    def __init__(self, max_health, ):
        self.max_health = max_health
        self.current_health = max_health

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

    def draw(self, surface, x, y, width, height):
        health_bar_width = (self.current_health / self.max_health) * width
        health_bar_rect = pg.Rect(x, y, health_bar_width, height)
        pg.draw.rect(surface, (255, 0, 0), health_bar_rect)
