import pygame as pg
from settings import TYLE_SIZE
from utils import load_image

class BackgroundTyle(pg.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft = position)

class Map:
    def __init__(self, layout):
        self.layout = layout
        self.dimensions = (len(layout[0]) * TYLE_SIZE, len(layout) * TYLE_SIZE)
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
                tyle = BackgroundTyle(
                    self.background_tyles[element],
                    (column_index * TYLE_SIZE, row_index * TYLE_SIZE)
                )
                self.background[row_index].append(tyle)
