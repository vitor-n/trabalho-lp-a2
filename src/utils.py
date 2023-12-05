import pygame as pg
from os.path import join
from settings import TYLE_SIZE

def load_image(image_path):
    image = pg.image.load(join(*image_path))
    image = image.convert_alpha()
    image = pg.transform.scale(image, (TYLE_SIZE, TYLE_SIZE))
    return image
