from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS, ENEMY_SPAWN_TIME
from player import Player
from utils import load_map
from map_ import Map
import sys
from camera import SmoothCamera
from weapons import Gun
from cursor import Cursor
from enemies import Apache, Roman, Samurai, Viking, IntegralGang

pg.init()
pg.mouse.set_visible(False)
clock = pg.time.Clock()
pg.display.set_caption("Guerreiros Integrais")
screen = pg.display.set_mode(SCREEN_DIMENSIONS)

map_layout = load_map("maps/map.json")["tiles"]
map = Map(map_layout)
player = Player(("Sprites", "Player", "player.png"), (0,0), map.dimensions)
cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5), player)
gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor)

gang = IntegralGang()
gang.create_group(Apache, 5, 3, 1, player.coords)

camera = SmoothCamera(screen, map, player, cursor.rect.center)
player.set_weapon(gun)
cursor.set_camera(camera)
delta_time = 0
curr_time = 0
last_time = 0

bullet_group = pg.sprite.Group()

while True:
    curr_time = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill("white")

    if curr_time - last_time > ENEMY_SPAWN_TIME:
        last_time = curr_time
        gang.create_group(Samurai, 5, 2, 1, player.rect)
 
    camera.update()
    player.update()
    gang.update(player.rect, delta_time)
    cursor.update()
    camera.render_map()
    camera.render_entity(player)
    camera.render_group(gang)
    camera.render_sprite_no_offset(cursor)

    #camera.render_group(gun.bullet_group)d
    camera.set_cursor_position(cursor.rect.center)

    pg.display.update()
    delta_time = clock.tick(FPS)
