import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE

class Camera:
    """
    Class representing the camera.
    The objective of this class is to center the process of choosing what is
    gonna be drawn and what not and calculating where in the screen something
    should be, based on the world position and the camera position.
    In this implementation, the camera is always above the player, but that can
    be changed if needed. Also, selecting what should be drawn can be as easy as
    using a pygame method to see if rectangles overlap, given the camera has an
    associated rectangle.

    Parameters
    ----------
    screen:
        The pygame Surface that represents the screen.
    map_:
        The map object with tile data.
    player:
        A player instance.
    """
    def __init__(self, screen, map_, player, gun):
        self.rect = pg.Rect(
            player.rect.x - SCREEN_DIMENSIONS[0] / 2,
            player.rect.y - SCREEN_DIMENSIONS[1] / 2,
            *SCREEN_DIMENSIONS
        )
        self.player = player
        self.map_ = map_
        self.map_tiles_to_render = pg.sprite.Group()
        self.screen = screen
        self.gun = gun


    def prepare_map_tiles(self):
        self.map_tiles_to_render.empty()
        for row in self.map_.background:
            for element in row:
                if self.rect.colliderect(element.rect):
                    self.map_tiles_to_render.add(element)

    def render(self):
        for sprite in self.map_tiles_to_render:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.rect.topleft[0], sprite.rect.topleft[1] - self.rect.topleft[1]))
        self.screen.blit(self.player.image, (self.player.rect.topleft[0] - self.rect.topleft[0], self.player.rect.topleft[1] - self.rect.topleft[1]))
        self.screen.blit(self.gun.image, (self.gun.rect.topleft[0] - self.rect.topleft[0], self.gun.rect.topleft[1] - self.rect.topleft[1]))

    def update(self):
        self.rect.center = self.player.rect.center


class SmoothCamera(Camera):
    def __init__(self, screen, map_, target, gun):
        super().__init__(screen, map_, target, gun)
        self.target = self.player
        self.smooth_speed = 6
        self.rect.center = (self.player.rect.centerx,self.player.rect.centery)
        self.direction = pg.math.Vector2()

    def set_target(self, target):
        self.target = target
    
    def update(self):
        self.direction.x = self.target.rect.centerx - self.rect.centerx
        self.direction.y = self.target.rect.centery - self.rect.centery
        if self.direction.magnitude_squared() != 0:
            self.direction = self.direction.normalize()
        self.rect.centerx += int(self.direction.x * self.smooth_speed)
        self.rect.centery += int(self.direction.y * self.smooth_speed)
