
from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS, ENEMY_SPAWN_TIME
from player import Player
from utils import load_map
from map_ import Map, RepeatMap
import sys
from camera import SmoothCamera
from weapons import SineShotgun
from cursor import Cursor
from enemies import Apache, Roman, Samurai, Viking, IntegralGang
from inventory import Inventory
from text import Font


class Game:
    def __init__(self, screen) -> None:

        self._screen = screen

        self._player = Player(("Sprites", "Player", "player.png"), (0,0), 2)
        map_layout = load_map("maps/map.json")["tiles"]
        self._map = RepeatMap(map_layout)

        self._font = Font(("Font", "pixel_font.png"))
        self._cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2), self._player)
        self._gun = SineShotgun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self._cursor)
        self._gang = IntegralGang()
        self._gang.create_group(Apache, 5, 3, 1, self._player.coords)
        self._camera = SmoothCamera(screen, self._map, self._player, self._cursor.rect.center)
        self._player.set_weapon(self._gun)
        self._cursor.set_camera(self._camera)
        self._cursor.set_owner(self._player)

        self.__on_game = False
        self._delta_time = 0
        self.__last_enemy_spawn_time = 0

    def update(self):
        curr_time = pg.time.get_ticks()

        if curr_time - self.__last_enemy_spawn_time > ENEMY_SPAWN_TIME:
            self.__last_enemy_spawn_time = curr_time
            self._gang.random_group(5, 2, 1, self._player.rect)

        self._camera.update()
        self._player.update()
        self._gang.update(self._player.rect, self._delta_time)
        self._cursor.update()
        self._map.expand(self._camera.rect)
        self._camera.render_map()
        self._font.render(self._screen, f"dash using space", (self._player.rect.centerx-self._camera.rect.topleft[0]-50, self._player.rect.top - self._camera.rect.topleft[1] - 50))
        self._camera.render_group(self._gang)
        self._camera.render_entity(self._player)
        self._camera.render_sprite_no_offset(self._cursor)

        #camera.render_group(gun.bullet_group)d
        self._camera.set_cursor_position(self._cursor.rect.center)
        self._camera.render_group(self._gun.bullet_group)

        self._screen.blit(self._player.health.bar, (33,30))

        self._font.render(self._screen, "time: 5:00", (33,90))
        self._font.render(self._screen, "sin(x)", (33,120))
        self._screen.blit(self._cursor.image, self._cursor.rect)


    def run(self):
        self.update()