import pygame
import os
import json
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)

SCREEN_DIMENSIONS = (1280, 720)
FPS = 60
PX_SCALE = 3
TILE_SIZE = 32 * PX_SCALE
FONT = pygame.font.Font(os.path.join("font", "essential.ttf"), 36)
ENEMY_SPAWN_TIME = 10*(1000)

with open(os.path.join("enemies", "integraldata.json"), 'r') as doc:
    integrals_info = json.load(doc)


HIT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "hit.wav"))
HIT_SOUND.set_volume(0.7)

DASH_SOUND = pygame.mixer.Sound(os.path.join("sounds", "dash.wav"))
DASH_SOUND.set_volume(1)

SHOOT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "dash.wav"))
SHOOT_SOUND.set_volume(1)

ZERO_GUN_STATS = {
    "move_function": lambda m: 0,
    "damage": 10,
    "mag_size": 1,
    "reload_cooldown": 500,
    "bullet_speed": 10,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

SINE_GUN_STATS = {
    "move_function": lambda m: -math.cos(m) * 40,
    "damage": 5,
    "mag_size": 30,
    "reload_cooldown": 2000,
    "bullet_speed": 15,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}

LINE_GUN_STATS = {
    "move_function": lambda m: 0,
    "damage": 2,
    "mag_size": 40,
    "reload_cooldown": 1500,
    "bullet_speed": 20,
    "bullet_sprite": ("Sprites", "bullets", "bullet1.png")
}
