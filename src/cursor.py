import pygame
from utils import load_image
import math
from settings import SCREEN_DIMENSIONS

class Cursor:
    def __init__(self, image_path, scale, position, player):
        self.player = player
        self.image = load_image(image_path, scale)
        self.rect = self.image.get_rect(center=position)
        self.angle_radians = 0
        self.angle_degrees = 0

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.angle_radians = math.atan2(self.player.rect.centery - self.rect.centery, self.rect.centerx - self.player.rect.centerx)
        self.angle_degrees = math.degrees(self.angle_radians)
        
        