import pygame as pg
from settings import TILE_SIZE
from utils import load_tile_image

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
    Class representing a map. It contains a grid with the tiles of the map.

    Parameters
    ----------
    layout:
        An matrix representing the tile placement in the map.
    """
    def __init__(self, layout):
        self._layout = layout
        self._background = pg.sprite.Group()
        self._load_images()
        self._create_map_background()

    @property
    def layout(self):
        """
        The layout the map needs to follow. Overriding it will automatically
        update the `background` property.
        """
        return self._layout

    @layout.setter
    def layout(self, layout):
        self._layout = layout
        self._create_map_background()

    @property
    def dimensions(self):
        """
        The dimensions, in pixels, of the background. It's important to notice
        that this isn't the map dimensions in tiles.
        """
        return (
            len(self._layout[0]) * TILE_SIZE,
            len(self._layout) * TILE_SIZE
        )

    @property
    def background(self):
        """
        A pygame group containing multiple tiles. The tiles are made based on
        `layout` and have correct positions.
        """
        return self._background

    def _load_images(self):
        self.background_tiles = {
            "1": "chao3",
            "2": "chao2",
            "3": "chao1"
        }
        for tile_identifier, filename in self.background_tiles.items():
            self.background_tiles[tile_identifier] = load_tile_image(("Sprites", "Provisory", f"{filename}.png"))

    def _create_map_background(self):
        self._background.empty()
        for row_index, row in enumerate(self._layout):
            for column_index, element in enumerate(row):
                tile = BackgroundTile(
                    self.background_tiles[element],
                    (column_index * TILE_SIZE, row_index * TILE_SIZE)
                )
                self._background.add(tile)
