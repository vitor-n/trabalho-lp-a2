from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS
from player import Player
from utils import load_image, load_map
from map_ import Map
import sys
from camera import Camera

pg.init
clock = pg.time.Clock()
pg.init()
screen = pg.display.set_mode(SCREEN_DIMENSIONS)
clock = pg.time.Clock()
map_layout = load_map('../trabalho-lp-a2/maps/map.json')["tiles"]
map = Map(map_layout)
player = Player(("..", "trabalho-lp-a2", "Sprites", "Player", "player.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5), map.dimensions)
camera = Camera(screen, map, player)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill('white')

    player.update()
    camera.update()
    camera.prepare_map_tiles()
    camera.render()

    pg.display.update()
    clock.tick(FPS)

