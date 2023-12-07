import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE
import math

class Camera:
    """
    Class representing a basic camera.
    The objective of this class is to center the process of choosing what is
    gonna be drawn and what not and calculating where in the screen something
    should be, based on the world position and the camera position.
    In this implementation, the camera is always above the target. Selecting
    what should be drawn can be as easy as using a pygame method to see if
    rectangles overlap, given the camera has an associated rectangle.

    Parameters
    ----------
    screen:
        The pygame Surface that represents the screen.
    map_:
        The map object with tile data.
    target:
        An entity to set the camera position.
    """
    def __init__(self, screen, map_, target):
        self.rect = pg.Rect(0, 0, *SCREEN_DIMENSIONS)
        self.target = target
        self.map_ = map_
        self.map_tiles_to_render = pg.sprite.Group()
        self.screen = screen

    def set_target(self, target):
        self.target = target

    def prepare_map_tiles(self):
        self.map_tiles_to_render.empty()
        for row in self.map_.background:
            for element in row:
                if self.rect.colliderect(element.rect):
                    self.map_tiles_to_render.add(element)

    def render_tiles(self):
        for sprite in self.map_tiles_to_render:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.rect.topleft[0], sprite.rect.topleft[1] - self.rect.topleft[1]))

    def render_player(self):
        self.screen.blit(self.target.image, (self.target.rect.topleft[0] - self.rect.topleft[0], self.target.rect.topleft[1] - self.rect.topleft[1]))
        if self.target.weapon:
            self.screen.blit(self.target.weapon.image, (self.target.weapon.rect.topleft[0] - self.rect.topleft[0], self.target.weapon.rect.topleft[1] - self.rect.topleft[1]))

    def render(self, source):
        self.screen.blit(source.image, (source.rect.topleft[0] - self.rect.topleft[0], source.rect.topleft[1] - self.rect.topleft[1]))
        
    def update(self):
        self.rect.center = self.target.rect.center


class SmoothCamera(Camera):
    """
    Class representing a camera with smooth movimentation.
    Instead of being always above the target, this camera moves smoothly to
    the target direction.
    Parameters
    ----------
    screen:
        The pygame Surface that represents the screen.
    map_:
        The map object with tile data.
    target:
        An entity to set the camera position.
    """
    def __init__(self, screen, map_, target):
        super().__init__(screen, map_, target)
        self.smooth_speed = 0.1

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        self.rect.centerx += int(dx * self.smooth_speed)
        self.rect.centery += int(dy * self.smooth_speed)
