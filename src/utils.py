import pygame as pg
import math
import json
from os.path import join
from settings import TILE_SIZE, PX_SCALE

def load_tile_image(image_path):
    """
        Loads an image from a file and scales it to the size of a tile.
    """
    image = pg.image.load(join(*image_path))
    image = image.convert_alpha()
    image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    return image

def load_image(image_path, scale = PX_SCALE):
    """
        Loads an image from a file and scales it by a factor of scale.
    """
    image = pg.image.load(join(*image_path))
    image = image.convert_alpha()
    image_height = image.get_height()
    image_width = image.get_width()
    image = pg.transform.scale(image, (image_width * scale, image_height * scale))
    return image

def load_map(filepath):
    """
        Loads a map from a json file.
    """
    with open(filepath, 'r') as file:
        map_layout = json.load(file)
    return map_layout

def angle_to(sprite1, sprite2):
    """
    Returns the angle (in radians) between two sprites.
    """
    x1, y1 = sprite1.rect.center
    x2, y2 = sprite2.rect.center
    return math.atan2(y1 - y2, x1 - x2)

def image_clip(surface, x, y, x_size, y_size):
    image_copy = surface.copy()
    clip = pg.Rect(x, y, x_size, y_size)
    image_copy.set_clip(clip)
    image = surface.subsurface(image_copy.get_clip())
    return image.copy()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)