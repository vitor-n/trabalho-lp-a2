import pygame

pygame.init()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Definição das dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Criação da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Título")

# Definição dos botões
button_width = 200
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2

# Loop principal do jogo
running = True
while running:
    # Verificação de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                print("Botão clicado!")

    # Preenchimento da tela com a cor preta
    screen.fill(BLACK)

    # Desenho do título
    font = pygame.font.Font(None, 64)
    text = font.render("Título do Jogo", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Verificação se o mouse está em cima do botão
    mouse_pos = pygame.mouse.get_pos()
    if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
        pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))

    # Atualização da tela
    pygame.display.flip()

# Encerramento do Pygame
pygame.quit()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definição das dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Criação da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Título")

# Definição dos botões
button_width = 200
button_height = 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2

# Loop principal do jogo
running = True
while running:
    # Verificação de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                print("Botão clicado!")

    # Preenchimento da tela com a cor preta
    screen.fill(BLACK)

    # Desenho do título
    font = pygame.font.Font(None, 64)
    text = font.render("Título do Jogo", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Desenho do botão
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))

    # Atualização da tela
    pygame.display.flip()

# Encerramento do Pygame
pygame.quit()

# Inicialização do Pygame
pygame.init()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definição das dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Criação da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela de Título")

# Loop principal do jogo
running = True
while running:
    # Verificação de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preenchimento da tela com a cor preta
    screen.fill(BLACK)

    # Desenho do título
    font = pygame.font.Font(None, 64)
    text = font.render("Título do Jogo", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Atualização da tela
    pygame.display.flip()

# Encerramento do Pygame
pygame.quit()
import pygame
