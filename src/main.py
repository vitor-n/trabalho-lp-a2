from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS, PX_SCALE
from player import Player
from utils import load_image, load_map
from map_ import Map
import sys
from camera import Camera
from weapons import Gun
from cursor import Cursor

pg.init()
pg.mouse.set_visible(False)
clock = pg.time.Clock()
pg.init()
screen = pg.display.set_mode(SCREEN_DIMENSIONS)
clock = pg.time.Clock()
map_layout = load_map('../trabalho-lp-a2/maps/map.json')["tiles"]
map = Map(map_layout)
player = Player(("..", "trabalho-lp-a2", "Sprites", "Player", "player.png"), (0,0), map.dimensions)
camera = Camera(screen, map, player)
cursor = Cursor(("..", "trabalho-lp-a2", "Sprites", "cursors", "cursor1.png"), 3, (TILE_SIZE* 9.5, TILE_SIZE*5.5), player)
gun = Gun(("..", "trabalho-lp-a2", "Sprites", "weapons", "player_weapons", "math_gun.png"), (SCREEN_DIMENSIONS[0]//2,SCREEN_DIMENSIONS[1]//2), cursor)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill('white')

    player.update()
    camera.update()
    gun.update()
    camera.prepare_map_tiles()
    camera.render()
    cursor.update()

    screen.blit(gun.image, gun.rect)
    screen.blit(cursor.image, cursor.rect)

    pg.display.update()
    clock.tick(FPS)

