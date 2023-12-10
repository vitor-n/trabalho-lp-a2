"""
This module contains the game class. This class is responsible for representing
a running instance of the game, aswell as implementing the game loop.
"""
from settings import SCREEN_DIMENSIONS, TILE_SIZE, ENEMY_SPAWN_TIME
from settings import ZERO_GUN_STATS, SINE_GUN_STATS, LINE_GUN_STATS, QUADRATIC_GUN_STATS
from player import Player, Inventory
from utils import load_map
from map_ import RepeatMap
from camera import SmoothCamera
from weapons import Gun
from cursor import Cursor
from enemies import IntegralGang
from text import Font

import pygame as pg
from pygame.locals import *

from random import randint
from enum import Enum

class GameDificulty(Enum):
    """
    Enum representing the possible game dificulties.
    """
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Game:
    """
    Class represents a running instance of a game. Every time the game should run,
    a instance of that class must be created. It holds a lot of instances from
    other objects, aswell as the game loop.

    Parameters
    ----------
    screen: pg.Surface
        The screen the game should run on.
    """
    def __init__(self, screen, game_dificulty = GameDificulty.EASY) -> None:

        self._screen = screen
        self._dificulty = game_dificulty

        map_layout = load_map("maps/map.json")["tiles"]
        self._map = RepeatMap(map_layout)

        self._font = Font(("font", "pixel_font_black.png"))
        self._font2 = Font(("font", "pixel_font_grey.png"))
        self._font3 = Font(("font", "pixel_font_white.png"))
        if self._dificulty is GameDificulty.EASY:
            initial_player_health = 8
        elif self._dificulty is GameDificulty.MEDIUM:
            initial_player_health = 6
        elif self._dificulty is GameDificulty.HARD:
            initial_player_health = 4
            SINE_GUN_STATS["reload_cooldown"] = 4000
        self._player = Player(("Sprites", "Player", "player.png"), (0,0), Inventory(), initial_player_health)
        self._cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5))

        self._gang = IntegralGang()
        self._camera = SmoothCamera(screen, self._map, self._player, self._cursor.rect.center)

        self._zero_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self._cursor, ZERO_GUN_STATS)
        self._sine_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self._cursor, SINE_GUN_STATS)
        self._line_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self._cursor, LINE_GUN_STATS)
        self._quadratic_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self._cursor, QUADRATIC_GUN_STATS)

        self._player.inventory.add_weapon(self._sine_gun, "sin(x)")
        self._player.inventory.add_weapon(self._zero_gun, "0")
        self._player.inventory.add_weapon(self._line_gun, "cx")
        self._player.inventory.add_weapon(self._quadratic_gun, "x@")

        self._delta_time = 0
        self._time_now = 0
        self._last_enemy_spawn_time = 0

        self._bullet_group = pg.sprite.Group()
        self._survival_time = 0
        self.menu_time = 0
        self.on_game = False

    def _render_entities(self):
        self._camera.render_entity(self._player)

    def _spawn_enemies(self):
        if self._time_now - (self._last_enemy_spawn_time) > ENEMY_SPAWN_TIME:
            self._last_enemy_spawn_time = self._time_now
            if self._dificulty is GameDificulty.EASY:
                self._gang.random_group(randint(4,6), randint(1,3), randint(0,0), self._player.rect)
            elif self._dificulty is GameDificulty.MEDIUM:
                self._gang.random_group(randint(5,8), randint(2,4), randint(0,2), self._player.rect)
            elif self._dificulty is GameDificulty.HARD:
                self._gang.random_group(randint(6,9), randint(4,5), randint(1,3), self._player.rect)
            self._gang.set_target_for_all(self._player)

    def _update(self, delta_time):
        self._delta_time = delta_time
        self._camera.render_map()
        self._camera.set_cursor_position(self._cursor.rect.center)
        self._camera.update()
        self._cursor.update()
        self._player.update((self._cursor.rect.centerx+self._camera.rect.topleft[0],self._cursor.rect.centery+self._camera.rect.topleft[1]))
        self._cursor.update()
        self._gang.update(self._delta_time, self._gang)
        self._map.expand(self._camera.rect)
        self._spawn_enemies()
        self._player_damage_handler()
        self._enemy_damage_handler()
        self._render_entities()
        self._render_hud()

    def _player_damage_handler(self):
        for weapon in self._player.inventory.get_weapons():
            damaged_enemies = pg.sprite.groupcollide(self._gang, weapon.bullet_group, False, True)
            for enemy in damaged_enemies:
                enemy.health - weapon.damage
                if enemy.health == 0:
                    enemy.kill()

    def _enemy_damage_handler(self):
        for enemy in self._gang:
            if enemy.weapon:
                if enemy.weapon.rect.colliderect(self._player.rect):
                    self._player.health - 1
                elif enemy.rect.colliderect(self._player.rect):
                    self._player.health - 1
                if hasattr(enemy.weapon, "bullet_group"):
                    if pg.sprite.spritecollide(self._player, enemy.weapon.bullet_group, True):
                        self._player.health - 1
            self._camera.render_entity(enemy)

    def _render_hud(self):
        self._screen.blit(self._player.health.bar, (33,30))
        self._font.render(self._screen, f"sobreviveu: {self._survival_time}s", (33,90))
        self._font.render(self._screen, self._dificulty.value, (1150, 33))

    def run(self, delta_time):
        """
        Run the game.

        Parameters
        ----------
        delta_time: float
            A variable that will hold the difference of time between every frame
            update.

        Returns
        -------
        None
        """
        self._time_now = pg.time.get_ticks()
        
        if self._player.health == 0:
            self._screen.fill("black")
            self._font3.render(self._screen, "GAME OVER!", (63, SCREEN_DIMENSIONS[1]//2-30))
            self._font3.render(self._screen, f"voce sobreviveu por: {self._survival_time} segundos", (63, SCREEN_DIMENSIONS[1]//2+30))
            self._font3.render(self._screen, f"voltando ao menu em {10-((self._time_now-self.menu_time)//1000-self._survival_time)} segundos", (63, SCREEN_DIMENSIONS[1]//2+90))
            
            if ((self._time_now - self.menu_time)//1000-self._survival_time) > 10:
                self.on_game = False
        else:
            self._survival_time = (self._time_now-self.menu_time)//1000
            self._update(delta_time)
    
