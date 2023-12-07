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
        self.rect = pg.Rect(
            target.rect.x - SCREEN_DIMENSIONS[0] / 2,
            target.rect.y - SCREEN_DIMENSIONS[1] / 2,
            *SCREEN_DIMENSIONS
        )
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

    def render(self):
        for sprite in self.map_tiles_to_render:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.rect.topleft[0], sprite.rect.topleft[1] - self.rect.topleft[1]))
        self.screen.blit(self.target.image, (self.target.rect.topleft[0] - self.rect.topleft[0], self.target.rect.topleft[1] - self.rect.topleft[1]))
        if self.target.weapon:
            self.screen.blit(self.target.weapon.image, (self.target.weapon.rect.topleft[0] - self.rect.topleft[0], self.target.weapon.rect.topleft[1] - self.rect.topleft[1]))

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
        self.smooth_speed = 6
        self.direction = pg.math.Vector2()

    def update(self):
        # Get vector with the direction the camera should go
        self.direction.x = self.target.rect.centerx - self.rect.centerx
        self.direction.y = self.target.rect.centery - self.rect.centery
        if self.direction.magnitude_squared() != 0:
            self.direction = self.direction.normalize()

        #Move the camera based on that vector and the speed
        self.rect.centerx += int(self.direction.x * self.smooth_speed)
        self.rect.centery += int(self.direction.y * self.smooth_speed)

        # If camera moves more than it needs, it may get in a state where it
        # never really center in the target. To avoid that, set the camera
        # coordinates to equal the target position if it passes the target
        new_direction_x = self.target.rect.centerx - self.rect.centerx
        new_direction_y = self.target.rect.centery - self.rect.centery
        if not math.copysign(1, new_direction_x) * math.copysign(1, self.direction.x) > 0:
            self.rect.centerx = self.target.rect.centerx
        if not math.copysign(1, new_direction_y) * math.copysign(1, self.direction.y) > 0:
            self.rect.centery = self.target.rect.centery

        # The target shouldnt get away from the camera, so if it does, the camera
        # gets repositioned so it shows the target
        if self.rect.right < self.target.rect.right:
            self.rect.right = self.target.rect.right
        elif self.rect.left > self.target.rect.left:
            self.rect.left = self.target.rect.left
        if self.rect.bottom < self.target.rect.bottom:
            self.rect.bottom = self.target.rect.bottom
        elif self.rect.top > self.target.rect.top:
            self.rect.top = self.target.rect.top
