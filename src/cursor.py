import pygame

class Cursor:
    def __init__(self, image_path):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy