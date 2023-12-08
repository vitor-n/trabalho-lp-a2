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
        self._map = map_
        self.screen = screen

    def set_target(self, target):
        self.target = target

    def update(self):
        self.rect.center = self.target.rect.center

    def calculate_offset(self, rectangle):
        return (rectangle.topleft[0] - self.rect.topleft[0],
               rectangle.topleft[1] - self.rect.topleft[1])

    def render_sprite(self, sprite):
        if self.rect.colliderect(sprite.rect):
            blit_coords = self.calculate_offset(sprite.rect)
            self.screen.blit(sprite.image, blit_coords)

    def render_sprite_no_offset(self, sprite):
        self.screen.blit(sprite.image, sprite.rect)

    def render_group(self, group):
        render_sprites = pg.sprite.spritecollide(self, group, False)
        for sprite in render_sprites:
            blit_coords = self.calculate_offset(sprite.rect)
            self.screen.blit(sprite.image, blit_coords)

    def render_group_no_offset(self, group):
        for sprite in group:
            self.screen.blit(sprite.image, sprite.rect)

    def render_map(self):
        self.render_group(self._map.background)

    def render_entity(self, entity):
        self.render_sprite(entity)
        if entity.weapon:
            self.render_sprite(entity.weapon)
            if hasattr(entity.weapon, "bullet_group"):
                self.render_group(entity.weapon.bullet_group)


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
    def __init__(self, screen, map_, target, cursor_pos):
        super().__init__(screen, map_, target)
        self.smooth_speed = 0.1
        self.cursor_pos = cursor_pos

    def set_cursor_position(self, cursor_pos):
        self.cursor_pos = cursor_pos

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery

        self.rect.centerx += int(dx * self.smooth_speed)
        self.rect.centery += int(dy * self.smooth_speed)

        self.rect.centerx += (self.cursor_pos[0] - SCREEN_DIMENSIONS[0] // 2) // 40
        self.rect.centery += (self.cursor_pos[1] - SCREEN_DIMENSIONS[1] // 2) // 40
