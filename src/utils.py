import pygame as pg
import json
from os.path import join
from settings import TILE_SIZE

def load_tile_image(image_path):
    image = pg.image.load(join(*image_path))
    image = image.convert_alpha()
    image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    return image

def load_image(image_path, scale):
    image = pg.image.load(join(*image_path))
    image = image.convert_alpha()
    image_height = image.get_height()
    image_width = image.get_width()
    image = pg.transform.scale(image, (image_width * scale, image_height * scale))
    return image

def load_map(filepath):
    with open(filepath, 'r') as file:
        map_layout = json.load(file)
    return map_layout