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
#from inventory import Inventory
from text import Font
import math

map_thing = [[str(divmod(50, 4)[1]) for i in range(400)] for i in range(400)]

zero_gun_stats = {
    "move_function": lambda m: 0,
    "damage": 10,
    "mag_size": 1,
    "reload_cooldown": 500,
    "bullet_speed": 10,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

sine_gun_stats = {
    "move_function": lambda m: math.sin(m) * 40,
    "damage": 5,
    "mag_size": 30,
    "reload_cooldown": 2000,
    "bullet_speed": 15,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

line_gun_stats = {
    "move_function": lambda m: 0,
    "damage": 2,
    "mag_size": 40,
    "reload_cooldown": 1500,
    "bullet_speed": 20,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

pg.init()
pg.mouse.set_visible(False)
clock = pg.time.Clock()
pg.display.set_caption("Guerreiros Integrais")
screen = pg.display.set_mode(SCREEN_DIMENSIONS)

map_layout = load_map("maps/map.json")["tiles"]
map = Map(map_thing)
teste = RepeatMap(map_layout)
font = Font(("font", "pixel_font_black.png"))
font2 = Font(("font", "pixel_font_grey.png"))
player = Player(("Sprites", "Player", "player.png"), (0,0), Inventory())
cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (TILE_SIZE* 9.5, TILE_SIZE*5.5))
zero_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor, zero_gun_stats)
sine_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor, sine_gun_stats)
line_gun = Gun(("Sprites", "weapons", "player_weapons", "math_gun.png"), cursor, line_gun_stats)
gang = IntegralGang()
gang.create_group(Apache, 5, 3, 1, player.coords, player)
camera = SmoothCamera(screen, teste, player, cursor.rect.center)
player.inventory.add_weapon(zero_gun, "0")
player.inventory.add_weapon(sine_gun, "sin(x)")
player.inventory.add_weapon(line_gun, "cx")
delta_time = 0
curr_time = 0
last_time = 0

bullet_group = pg.sprite.Group()

inventory = Inventory()
while True:
    curr_time = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[K_ESCAPE]:
            pg.quit()
            sys.exit()

    screen.fill("white")

    if curr_time - last_time > ENEMY_SPAWN_TIME:
        last_time = curr_time
        gang.random_group(5, 2, 1, player.rect, player)
 
    camera.update()
    player.update((cursor.rect.centerx+camera.rect.topleft[0],cursor.rect.centery+camera.rect.topleft[1]))
    gang.update(delta_time, gang)
    cursor.update()
    teste.expand(camera.rect)
    camera.render_map()
    font.render(screen, f"dash using space", (player.rect.centerx-camera.rect.topleft[0]-50, player.rect.top - camera.rect.topleft[1] - 50))
    camera.render_entity(player)
    for integral in gang:
        camera.render_entity(integral)
    camera.render_sprite_no_offset(cursor)

    for enemy in gang:
        if enemy.weapon:
            if enemy.weapon.rect.colliderect(player.rect):
                player.health - 1
            elif enemy.rect.colliderect(player.rect):
                player.health - 1
            if hasattr(enemy.weapon, "bullet_group"):
                if pg.sprite.spritecollide(player, enemy.weapon.bullet_group, True):
                    player.health - 1

    damaged_enemies = pg.sprite.groupcollide(gang, player.weapon.bullet_group, False, True)

    for enemy in damaged_enemies:
        enemy.health - 1

    camera.set_cursor_position(cursor.rect.center)

    screen.blit(player.health.bar, (33,30))
    font.render(screen, "time: 5:00", (33,90))
    screen.blit(cursor.image, cursor.rect)


    #pg.draw.line(screen, (255, 0, 0), (0, SCREEN_DIMENSIONS[1] // 2), (SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1] // 2), 1)
    #pg.draw.line(screen, (255, 0, 0), (SCREEN_DIMENSIONS[0] // 2, 0), (SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1]), 1)

    pg.display.update()
    delta_time = clock.tick(FPS)
