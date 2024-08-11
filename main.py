"""
The module that will call all the necessary classes to make the game start.
"""
import pygame
from src.settings import SCREEN_DIMENSIONS
from src.menu import Menu
from src.game import Game
from src.cursor import Cursor

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load("sounds/ironmain.wav")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Guerreiros Integrais")
pygame.mouse.set_visible(False)

menu = Menu(screen)
game = Game(screen)

cursor = Cursor(("Sprites", "cursors", "cursor2.png"), (SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))

while True:

    click = False

    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        quit()

    screen.fill("white")

    cursor.update()

    if menu.on_menu:
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            if event.button == 1:
                click = True
        menu.update(click)
        if not menu.on_menu:
            game = Game(screen, menu.selected_difficulty)
            game.on_game = True
            game.menu_time = pygame.time.get_ticks()
    if game.on_game:
        game.run(delta_time)
        if not game.on_game:
            game = Game(screen, menu.selected_difficulty)
            menu.on_menu = True
            menu.on_titlescreen = True
            menu.on_config_menu = False

    screen.blit(cursor.image, cursor.rect)

    pygame.display.update()
    delta_time = clock.tick(60)


