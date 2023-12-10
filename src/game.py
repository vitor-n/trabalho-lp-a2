from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS, ENEMY_SPAWN_TIME
from player import Player, Inventory
from utils import load_map
from map_ import Map, RepeatMap
import sys
from camera import SmoothCamera
from weapons import Gun
from cursor import Cursor
from enemies import Apache, Roman, Samurai, Viking, IntegralGang
from text import Font
from settings import ZERO_GUN_STATS, SINE_GUN_STATS, LINE_GUN_STATS, QUADRATIC_GUN_STATS
from random import randint


class Game:
    def __init__(self, screen) -> None:

        self._screen = screen

        map_layout = load_map("maps/map.json")["tiles"]
        self._map = RepeatMap(map_layout)

        self._font = Font(("font", "pixel_font_black.png"))
        self._font2 = Font(("font", "pixel_font_grey.png"))

        self._player = Player(("Sprites", "Player", "player.png"), (0,0), Inventory())
        self._cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5))

        self._gang = IntegralGang()
        self._camera = SmoothCamera(screen, self._map, self._player, self._cursor.rect.center)
        
        self.zero_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, ZERO_GUN_STATS)
        self.sine_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, SINE_GUN_STATS)
        self.line_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, LINE_GUN_STATS)
        self.quadratic_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, QUADRATIC_GUN_STATS)

        self.player.inventory.add_weapon(self.zero_gun, "0")
        self.player.inventory.add_weapon(self.sine_gun, "sin(x)")
        self.player.inventory.add_weapon(self.line_gun, "cx")
        self.player.inventory.add_weapon(self.quadratic_gun, "x@")

        self._delta_time = 0
        self._time_now = 0
        self._last_enemy_spawn_time = 0

        self._bullet_group = pg.sprite.Group()
        
        self.menu_time = 0
        self.on_game = False

    def _render_entities(self):
        self._camera.render_entity(self._player)

    def _spawn_enemies(self):
        if self._time_now - (self._last_enemy_spawn_time+self.menu_time) > ENEMY_SPAWN_TIME:
            self._last_enemy_spawn_time = self._time_now
            self._gang.random_group(randint(2,5), randint(2,3), randint(1,2), self._player.rect)
            self._gang.set_target_for_all(self._player)

    def _update(self):
        self._time_now = pg.time.get_ticks()
        self._camera.set_cursor_position(self._cursor.rect.center)
        self._camera.update()
        self._cursor.update()
        self._player.update((self._cursor.rect.centerx+self._camera.rect.topleft[0],self._cursor.rect.centery+self._camera.rect.topleft[1]))
        self._cursor.update()
        self._gang.update(self._delta_time, self._gang)
        self._map.expand(self._camera.rect)

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
        self._font.render(self._screen, f"sobreviveu: {(self._time_now-self.menu_time)//1000}s", (33,90))
        print(self._time_now-self.menu_time)
    def run(self, delta_time):
        self._delta_time = delta_time
        self._camera.render_map()
        self._update()
        self._spawn_enemies()
        self._player_damage_handler()
        self._enemy_damage_handler()
        self._render_entities()
        self._render_hud()