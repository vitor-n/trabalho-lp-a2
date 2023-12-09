from pygame.locals import *
import pygame as pg
from settings import SCREEN_DIMENSIONS, TILE_SIZE, FPS
from player import Player
from utils import load_map
from map_ import Map, RepeatMap
import sys
from camera import SmoothCamera
from weapons import SineShotgun
from cursor import Cursor
from enemies import Apache
from inventory import Inventory
from text import Font

map_thing = [[str(divmod(50, 4)[1]) for i in range(400)] for i in range(400)]

pg.init()
pg.mouse.set_visible(False)
clock = pg.time.Clock()
pg.display.set_caption("Guerreiros Integrais")
screen = pg.display.set_mode(SCREEN_DIMENSIONS)

map_layout = load_map("maps/map.json")["tiles"]
map = Map(map_thing)
teste = RepeatMap(map_layout)
font = Font(("Font", "pixel_font.png"))
player = Player(("Sprites", "Player", "player.png"), (0,0), (map.rect.width, map.rect.height))
cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5), player)
gun = SineShotgun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor)
enemy = Apache((0,10), 2)
enemy2 = Apache((0,20), 1)
camera = SmoothCamera(screen, teste, player, cursor.rect.center)
player.set_weapon(gun)
cursor.set_camera(camera)
delta_time = 0

bullet_group = pg.sprite.Group()

inventory = Inventory()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill("white")

    enemy.update(player.rect, delta_time)
    enemy2.update(player.rect, delta_time)
    camera.update()
    player.update()
    cursor.update()
    teste.expand(camera.rect)
    camera.render_map()
    camera.render_entity(player)
    camera.render_sprite(enemy)
    camera.render_sprite_no_offset(cursor)

    #camera.render_group(gun.bullet_group)d
    camera.set_cursor_position(cursor.rect.center)
    camera.render_group(gun.bullet_group)

    screen.blit(player.health.bar, (30,30))
    screen.blit(inventory.sine_gun, (30,120))
    screen.blit(cursor.image, cursor.rect)

    font.render(screen, "time: 5:00", (30,90))

    #pg.draw.line(screen, (255, 0, 0), (0, SCREEN_DIMENSIONS[1] // 2), (SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1] // 2), 1)
    #pg.draw.line(screen, (255, 0, 0), (SCREEN_DIMENSIONS[0] // 2, 0), (SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1]), 1)

    pg.display.update()
    delta_time = clock.tick(FPS)
