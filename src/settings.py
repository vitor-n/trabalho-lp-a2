import pygame
import os
import json

pygame.init()

SCREEN_DIMENSIONS = (1280, 720)
FPS = 60
PX_SCALE = 3
TILE_SIZE = 32 * PX_SCALE
FONT = pygame.font.Font(os.path.join("Font", "Essential.ttf"), 36)
ENEMY_SPAWN_TIME = 10*(1000)

with open(os.path.join("dados", "dadosintegrais.json"), 'r') as doc:
    integrals_info = json.load(doc)


