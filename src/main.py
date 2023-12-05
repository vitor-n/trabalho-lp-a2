import pygame as pg
from settings import SCREEN_DIMENSIONS, TYLE_SIZE, FPS
from player import Player
from utils import load_image
import sys

class Map:
    def __init__(self, layout):
        self.layout = layout
        self.dimensions = (len(layout[0]) * TYLE_SIZE, len(layout) * TYLE_SIZE)
        self.create_map_background()

    def create_map_background(self):
        self.background = pg.Surface(self.dimensions)
        background_tyles = {
            "1": "chao3",
            "2": "chao2",
            "3": "chao1"
        }
        for tyle_identifier, filename in background_tyles.items():
            background_tyles[tyle_identifier] = load_image(("Sprites", "Provisory", f"{filename}.png"))
        for row_index, row in enumerate(self.layout):
            for column_index, element in enumerate(row):
                self.background.blit(background_tyles[element], (column_index * TYLE_SIZE, row_index * TYLE_SIZE))



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS)
        self.clock = pg.time.Clock()
        map_layout = [
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "3", "1", "3", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "3", "1", "3", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "3", "1", "3", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "2", "2", "2", "2"],
        ]
        self.map = Map(map_layout)

    def run(self):
        player = Player(("..", "trabalho-lp-a2", "Sprites", "Jogo_Integrais", "apache_tripleint.png"), (TYLE_SIZE* 9.5, TYLE_SIZE*5.5), self.map.dimensions)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill('black')

            player.update()
            self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y))
            if player.rect.x < SCREEN_DIMENSIONS[0]/2 and player.rect.y < SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x - self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y - self.map.dimensions[1]))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x - self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y - self.map.dimensions[1]))
            elif player.rect.x < SCREEN_DIMENSIONS[0]/2 and player.rect.y > self.map.dimensions[1] - SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x - self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y + self.map.dimensions[1]))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x - self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y + self.map.dimensions[1]))
            elif player.rect.x > self.map.dimensions[0] - SCREEN_DIMENSIONS[0]/2 and player.rect.y < SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x + self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y - self.map.dimensions[1]))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x + self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y - self.map.dimensions[1]))
            elif player.rect.x > self.map.dimensions[0] - SCREEN_DIMENSIONS[0]/2 and player.rect.y > self.map.dimensions[1] - SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x + self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y + self.map.dimensions[1]))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x + self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y + self.map.dimensions[1]))
            elif player.rect.x > self.map.dimensions[0] - SCREEN_DIMENSIONS[0]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x + self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
            elif player.rect.y > self.map.dimensions[1] - SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y + self.map.dimensions[1]))
            elif player.rect.x < SCREEN_DIMENSIONS[0]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x - self.map.dimensions[0], SCREEN_DIMENSIONS[1]/2 - player.rect.y))
            elif player.rect.y < SCREEN_DIMENSIONS[1]/2:
                self.screen.blit(self.map.background, (SCREEN_DIMENSIONS[0]/2 - player.rect.x, SCREEN_DIMENSIONS[1]/2 - player.rect.y - self.map.dimensions[1]))

            self.screen.blit(player.image, (TYLE_SIZE* 9, TYLE_SIZE*5))

            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()



