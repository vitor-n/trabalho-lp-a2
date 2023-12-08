import pygame
from utils import load_image
import math

class Cursor:
    def __init__(self, image_path, initial_position, player):
        self.player = player
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(center = initial_position)
        self.angle_radians = 0
        self.angle_degrees = 0

    def set_camera(self, camera):
        self.camera = camera

    def update(self):
        player_position_screen_space = (
            self.player.rect.center[0] - self.camera.rect.topleft[0],
            self.player.rect.center[1] - self.camera.rect.topleft[1],
        )
        
        self.rect.center = pygame.mouse.get_pos()
        self.angle_radians = math.atan2(player_position_screen_space[1] - self.rect.centery, self.rect.centerx - player_position_screen_space[0])
        self.angle_degrees = math.degrees(self.angle_radians)

        
