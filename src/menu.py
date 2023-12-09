import pygame 
from settings import FPS, FONT, SCREEN_DIMENSIONS
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))
pygame.display.set_caption("Guerreiros Integrais")
clock = pygame.time.Clock()

# Load game title image
game_title_image = pygame.image.load(r"Sprites/Menu/title.png")  
game_title_rect = game_title_image.get_rect() 

# Load button images
play_button_image = pygame.image.load(r"Sprites/Menu/play_button.png")  
config_button_image = pygame.image.load(r"Sprites/Menu/config_button.png")  

config_button_rect = config_button_image.get_rect(topleft=(SCREEN_DIMENSIONS[0] // 2 - config_button_image.get_width() // 2, SCREEN_DIMENSIONS[1] // 2 + 100))
play_button_rect = play_button_image.get_rect(topleft=(SCREEN_DIMENSIONS[0] // 2 - play_button_image.get_width() // 2, SCREEN_DIMENSIONS[1] // 2 + 10))

# Function to display text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Function for the main menu screen
def main_menu():
    while True:
        screen.fill((0,0,0))
        
        # Draw the game title image
        screen.blit(game_title_image, (SCREEN_DIMENSIONS[0]// 2 - game_title_rect.width // 2, SCREEN_DIMENSIONS[1] // 4 - game_title_rect.height // 2))
        
        # Draw button images
        screen.blit(play_button_image, (SCREEN_DIMENSIONS[0] // 2 - play_button_image.get_width() // 2, SCREEN_DIMENSIONS[1] // 2 + 10))
        screen.blit(config_button_image, (SCREEN_DIMENSIONS[0] // 2 - config_button_image.get_width() // 2, SCREEN_DIMENSIONS[1] // 2 + 100))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    print('PRINT PLAY')
                    return "play"
                elif config_button_rect.collidepoint(mouse_pos):
                    print("config, sem print")
                    return "config"
            
        pygame.display.flip()
     
# Function for the configuration screen
def config_menu():
    while True:
        screen.fill((0,0,0))
        draw_text("Selecione a dificuldade.", FONT, (255,255,255), screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 4)

        # Difficulty buttons
        easy_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2, 200, 50)
        normal_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2 + 70, 200, 50)
        hard_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2 + 140, 200, 50)

        pygame.draw.rect(screen, (255,255,255), easy_button)
        draw_text("Fácil", FONT, (0,0,0), screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 25)
        pygame.draw.rect(screen, (255,255,255), normal_button)
        draw_text("Normal", FONT, (0,0,0), screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 95)
        pygame.draw.rect(screen, (255,255,255), hard_button)
        draw_text("Difícil", FONT, (0,0,0), screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 165)

        # Event handling for difficulty selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    return "easy"
                elif normal_button.collidepoint(mouse_pos):
                    return "normal"
                elif hard_button.collidepoint(mouse_pos):
                    return "hard"

        pygame.display.flip()
        clock.tick(FPS)
        
# Main function to control flow
def main():
    while True:
        choice = main_menu()
        
        if choice == "config":
            difficulty = config_menu() #mudar constantes de dificuldade
            
    

if __name__ == "__main__":
    main()