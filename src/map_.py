"""
This module is responsible for defining classes to represent the map. The two
types of maps are made with tiles, that are also implemented here. The file
containing the map data is located inside map folder, and to declare a map a list
of lists is used.
"""
from settings import TILE_SIZE
from utils import load_tile_image

import pygame as pg

class BackgroundTile(pg.sprite.Sprite):
    """
    Class representing a tile of the map. A tile is a square that is part of the
    map background.

    Parameters
    ----------
    image: pg.surface.Surface
        A pygame image object. It should be previously scaled to tile size.
    position: tuple
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
    layout: list
        An matrix representing the tile placement in the map.
    """
    def __init__(self, layout):
        self._layout = layout
        self._background = pg.sprite.Group()
        self._load_images()
        self._create_map_background()

    @property
    def layout(self) -> list:
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
    def dimensions(self) -> tuple:
        """
        The dimensions, in pixels, of the background. It's important to notice
        that this isn't the map dimensions in tiles.
        """
        return (
            len(self._layout[0]) * TILE_SIZE,
            len(self._layout) * TILE_SIZE
        )

    @property
    def rect(self) -> pg.Rect:
        """
        A rectangle representing the map boundaries. It's dimensions represent
        the dimensions of the map in pixels, not in tiles.
        """
        return pg.Rect(
            0, 0,
            len(self._layout[0]) * TILE_SIZE,
            len(self._layout) * TILE_SIZE
        )

    @property
    def background(self) -> pg.sprite.Group:
        """
        A pygame group containing multiple tiles. The tiles are made based on
        `layout` and have correct positions.
        """
        return self._background

    def _load_images(self):
        self.background_tiles = {
            "1": "tile1",
            "2": "tile2",
            "3": "tile3",
            "4": "tile4",
            "5": "tile5",
            "6": "tile_doodle_1",
            "7": "tile_doodle_2",
            "8": "tile_doodle_3",
            "9": "tile_doodle_4",
            "10": "tile_doodle_5"
        }
        for tile_identifier, filename in self.background_tiles.items():
            self.background_tiles[tile_identifier] = load_tile_image(("Sprites", "tiles", f"{filename}.png"))

    def _create_map_background(self):
        self._background.empty()
        for row_index, row in enumerate(self._layout):
            for column_index, element in enumerate(row):
                tile = BackgroundTile(
                    self.background_tiles[element],
                    (column_index * TILE_SIZE, row_index * TILE_SIZE)
                )
                self._background.add(tile)


class RepeatMap(Map):
    """
    Class representing a repeating map. It contains a grid with the tiles of the
    map. This class is capable of moving some map tiles to other side, creating
    a illusion of an infinite map

    Parameters
    ----------
    layout: list
        An matrix representing the tile placement in the map. Every new part of
        the map will be moved based on that.
    """
    def __init__(self, layout):
        super().__init__(layout)
        self._top = 0
        self._bottom = self.dimensions[1]
        self._left = 0
        self._right = self.dimensions[0]

    def expand(self, rect):
        """
        Updates the map, based in a rectangle, so it covers all the space in the
        rectangle with tiles. The tiles are moved from one border to another,
        so the number of tiles never change at all.

        Parameters
        ----------
        rect: pg.Rect
            The rectangle to use to move the map

        Returns
        -------
            None
        """
        if rect.right > self._right:
            for x in range(self._left, rect.right - self.dimensions[0], TILE_SIZE):
                line = (x, self._top, x, self._bottom)
                for tile in self._background:
                    if tile.rect.clipline(*line):
                        tile.rect.x += self.dimensions[0]
                self._right += TILE_SIZE
                self._left += TILE_SIZE
        elif rect.left < self._left:
            for x in range(-self._right + TILE_SIZE, -rect.left - self.dimensions[0] + TILE_SIZE, TILE_SIZE):
                line = (-x, self._top, -x, self._bottom)
                for tile in self._background:
                    if tile.rect.clipline(*line):
                        tile.rect.x -= self.dimensions[0]
                self._right -= TILE_SIZE
                self._left -= TILE_SIZE
        if rect.bottom > self._bottom:
            for y in range(self._top, rect.bottom - self.dimensions[1], TILE_SIZE):
                line = (self._right, y, self._left, y)
                for tile in self._background:
                    if tile.rect.clipline(*line):
                        tile.rect.y += self.dimensions[1]
                self._top += TILE_SIZE
                self._bottom += TILE_SIZE
        elif rect.top < self._top:
            for y in range(-self._bottom + TILE_SIZE, -rect.top - self.dimensions[1] + TILE_SIZE, TILE_SIZE):
                line = (self._right, -y, self._left, -y)
                for tile in self._background:
                    if tile.rect.clipline(*line):
                        tile.rect.y -= self.dimensions[1]
                self._top -= TILE_SIZE
                self._bottom -= TILE_SIZE

    @property
    def rect(self) -> pg.Rect:
        """
        A rectangle representing the map boundaries. It's dimensions represent
        the dimensions of the map in pixels, not in tiles.
        """
        return pg.Rect(
            self.top, self.left,
            len(self._layout[0]) * TILE_SIZE,
            len(self._layout) * TILE_SIZE
        )
"""
class AutoGeneratedMap(Map):
    def __init__(self, layout = None):
        if layout:
            super().__init__(layout)
        else:
            super().__init__([[]])
        self.last_update = (0, 0)

    def _expand(self, rect):
        expand_from = (
            rect.x - TILE_SIZE * 3 - divmod(rect.x, TILE_SIZE)[1],
            rect.y - TILE_SIZE * 3 - divmod(rect.y, TILE_SIZE)[1],
        )
        expand_size = (
            rect.width + TILE_SIZE * 6,
            rect.height + TILE_SIZE * 6
        )
        for x in range(expand_from[0], expand_size[0], TILE_SIZE):
            for y in range(expand_from[1], expand_size[1], TILE_SIZE):
                for tile in self._background:
                    if tile.rect.collidepoint(x, y):
                        break
                else:
                    tile = BackgroundTile(
                        self.background_tiles[random.choice(["1", "2", "3", "4"])],
                        (x, y)
                    )
                    self._background.add(tile)

    def _trim(self, rect):
        erase_distance = TILE_SIZE * 60
        for tile in self._background:
            if abs(rect.x - tile.rect.x) > erase_distance or abs(rect.y - tile.rect.y) > erase_distance:
                tile.kill()

    def update(self, rect):
        if abs(self.last_update[0] - rect.x) > TILE_SIZE or abs(self.last_update[1] - rect.y) > TILE_SIZE:
            self._expand(rect)
            #self._trim(rect)
            self.last_update = rect.topleft
"""
