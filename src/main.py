from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS
from player import Player
from utils import load_map
from map_ import Map
import sys
from camera import SmoothCamera
from weapons import Gun
from cursor import Cursor
from enemies import Apache

pg.init()
pg.mouse.set_visible(False)
clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_DIMENSIONS)

map_layout = load_map("maps/map.json")["tiles"]
map = Map(map_layout)
player = Player(("Sprites", "Player", "player.png"), (0,0), map.dimensions)
cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5), player)
gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor)
enemy = Apache((0,10), 2)
enemy2 = Apache((0,20), 1)
camera = SmoothCamera(screen, map, player, cursor.rect.center)
player.set_weapon(gun)
cursor.set_camera(camera)
delta_time = 0

bullet_group = pg.sprite.Group()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill("white")

    #enemy.update(player.rect, delta_time)
    #enemy2.update(player.rect, delta_time)
    camera.update()
    player.update()
    cursor.update()
    camera.render_map()
    camera.render_entity(player)
    #camera.render_sprite(enemy)
    camera.render_sprite_no_offset(cursor)

    #camera.render_group(gun.bullet_group)d
    camera.set_cursor_position(cursor.rect.center)

    pg.display.update()
    delta_time = clock.tick(FPS)
