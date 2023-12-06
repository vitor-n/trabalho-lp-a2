import pygame as pg
from settings import TILE_SIZE
from utils import load_image

class BackgroundTile(pg.sprite.Sprite):
    """
    Class representing a tile of the map. A tile is a square that is part of the
    map background.

    Parameters
    ----------
    image:
        A pygame image object. It should be previously scaled to tile size.
    position:
        The position of the tile in the world.
    """
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = position)

class Map:
    """
    Class representing the map. It contains a grid with the tiles of the map.

    Parameters
    ----------
    layout:
        An matrix representing the tile placement in the map.
    """
    def __init__(self, layout):
        self.layout = layout
        self.dimensions = (len(layout[0]) * TILE_SIZE, len(layout) * TILE_SIZE)
        self.load_images()
        self.create_map_background()

    def load_images(self):
        self.background_tyles = {
            "1": "chao3",
            "2": "chao2",
            "3": "chao1"
        }
        for tyle_identifier, filename in self.background_tyles.items():
            self.background_tyles[tyle_identifier] = load_image(("Sprites", "Provisory", f"{filename}.png"))

    def create_map_background(self):
        self.background = list()
        for row_index, row in enumerate(self.layout):
            self.background.append(list())
            for column_index, element in enumerate(row):
                tyle = BackgroundTile(
                    self.background_tyles[element],
                    (column_index * TILE_SIZE, row_index * TILE_SIZE)
                )
                self.background[row_index].append(tyle)