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
from settings import ZERO_GUN_STATS, SINE_GUN_STATS, LINE_GUN_STATS


class Game:
    def __init__(self, screen) -> None:

        self.screen = screen

        map_layout = load_map("maps/map.json")["tiles"]
        self.map = RepeatMap(map_layout)
        self.font = Font(("Font", "pixel_font_black.png"))
        self.font2 = Font(("Font", "pixel_font_grey.png"))
        self.player = Player(("Sprites", "Player", "player.png"), (0,0), Inventory())
        self.cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5))
        self.gang = IntegralGang()
        self.camera = SmoothCamera(screen, self.map, self.player, self.cursor.rect.center)
        
        self.zero_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, ZERO_GUN_STATS)
        self.sine_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, SINE_GUN_STATS)
        self.line_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), self.cursor, LINE_GUN_STATS)
        self.player.inventory.add_weapon(self.zero_gun, "0")
        self.player.inventory.add_weapon(self.sine_gun, "sin(x)")
        self.player.inventory.add_weapon(self.line_gun, "cx")

        self.delta_time = 0
        self.curr_time = 0
        self.__last_enemy_spawn_time = 0

        self.bullet_group = pg.sprite.Group()

        self.inventory = Inventory()

    @property
    def on_game(self):
        return self.__on_game

    def update(self):
        

        curr_time = pg.time.get_ticks()
        if curr_time - self.__last_enemy_spawn_time > ENEMY_SPAWN_TIME:
            self.__last_enemy_spawn_time = curr_time
            self.gang.random_group(5, 2, 1, self.player.rect)
            self.gang.set_target_for_all(self.player)
 
        self.camera.update()
        self.player.update((self.cursor.rect.centerx+self.camera.rect.topleft[0],self.cursor.rect.centery+self.camera.rect.topleft[1]))
        self.gang.update(self.delta_time, self.gang)
        self.cursor.update()
        self.map.expand(self.camera.rect)
        self.camera.render_map()
        self.camera.render_entity(self.player)
        self.camera.render_group(self.gang)
        self.camera.render_sprite_no_offset(self.cursor)

        for enemy in self.gang:
            if enemy.weapon:
                if enemy.weapon.rect.colliderect(self.player):
                    self.player.health - 1
                if hasattr(enemy.weapon, "bullet_group"):
                    if pg.sprite.spritecollide(self.player, enemy.weapon.bullet_group, True):
                        self.player.health - 1
        #if pg.sprite.spritecollide(self.player, self.gang, False, pg.sprite.collide_rect_ratio(0.7)):
        #    self.player.health - 1

        self.camera.set_cursor_position(self.cursor.rect.center)
        self.camera.render_group(self.zero_gun.bullet_group)
        self.camera.render_group(self.sine_gun.bullet_group)
        self.camera.render_group(self.line_gun.bullet_group)

        self.screen.blit(self.player.health.bar, (33,30))
        self.font.render(self.screen, "time: 5:00", (33,90))
        self.screen.blit(self.cursor.image, self.cursor.rect)

    def run(self):
        self.update()
