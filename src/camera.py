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
        self._map_ = map_
        self.screen = screen
        self.map_tiles_to_render = pg.sprite.Group()

    def set_target(self, target):
        self.target = target


    def calculate_offset(self, rectangle):
        return (rectangle.topleft[0] - self.rect.topleft[0],
               rectangle.topleft[1] - self.rect.topleft[1])

    def render_sprite(self, sprite):
        if self.rect.colliderect(sprite.rect):
            blit_coords = self.calculate_offset(sprite.rect)
            self.screen.blit(sprite.image, blit_coords)

    def render_sprite_no_offset(self, sprite):
        self.screen.blit(sprite.image, sprite.rect)

    def render_grouṕ(self, group):
        render_sprites = pg.sprite.spritecollide(self, group)
        for sprite in render_sprites:
            blit_coords = self.calculate_offset(sprite.rect)
            self.screen.blit(sprite.image, blit_coords)

    def render_group_no_offset(self, group):
        for sprite in group:
            self.screen.blit(sprite.image, sprite.rect)



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
        
    def render_group(self, source_group):
        for item in source_group:
            self.screen.blit(item.image, (item.rect.topleft[0] - self.rect.topleft[0], item.rect.topleft[1] - self.rect.topleft[1]))
            
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
