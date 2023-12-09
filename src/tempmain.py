import pygame
from settings import SCREEN_DIMENSIONS
from menu import Menu
from game import Game

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Guerreiros Integrais")
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

menu = Menu(screen)
game = Game(screen)

while True:

    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = True

    screen.fill("white")

    if menu.on_menu:
        menu.update(click)
    else:
        game.run()

    pygame.display.update()
    clock.tick(60)
    

