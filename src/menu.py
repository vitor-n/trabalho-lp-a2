import pygame 
from settings import FONT, SCREEN_DIMENSIONS
from utils import load_image, draw_text

class Menu:
    """
    Contains functions that create the menu and handle user interaction.
    """
    
    def __init__(self, screen) -> None:
        """
        Creates menu buttons and game title.

        Args:
            screen (pygame.display): screen shown to the player
        """
        self.screen = screen

        # Load game menu images
        self.game_title_image = load_image(("Sprites","Menu","title.png"), 1)  
        self.play_button_image = load_image(("Sprites","Menu","play_button.png"), 1)  
        self.config_button_image = load_image(("Sprites","Menu","config_button.png"), 1)

        self.game_title_rect = self.game_title_image.get_rect(center=(SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 4)) 
        self.play_button_rect = self.play_button_image.get_rect(center=(SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 10))
        self.config_button_rect = self.config_button_image.get_rect(center=(SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 100))
        
        #Create difficulty buttons
        self.easy_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2, 200, 50)
        self.normal_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2 + 70, 200, 50)
        self.hard_button = pygame.Rect(SCREEN_DIMENSIONS[0] // 2 - 100, SCREEN_DIMENSIONS[1] // 2 + 140, 200, 50)

        self.selected_difficulty = "normal"
        self.on_titlescreen = True
        self.on_config_menu = False
        self.titlescreen_choice = None

        self.on_menu = True
    
    def handle_quit_event(self):
        """
        Closes the window in case the player presses quit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


    def handle_titlescreen_events(self, click):
        """
        Process user input during the title screen phase.

        Args:
            click (bool): Indicates whether a mouse click event occurred.
        """
        if click:
            mouse_pos = pygame.mouse.get_pos()
            
            #If click on "play" button, go to game
            if self.play_button_rect.collidepoint(mouse_pos):
                self.titlescreen_choice = "play"
                self.on_titlescreen = False
                self.on_config_menu = False
                self.on_menu = False
            #Else if click on "config" button, go to configurations
            elif self.config_button_rect.collidepoint(mouse_pos):
                self.titlescreen_choice = "config"
                self.on_titlescreen = False
                self.on_config_menu = True


    def handle_config_menu_events(self, click):
        """
        Process user input during the configuration menu phase.

        Args:
            click (bool): Indicates whether a mouse click event occurred.
        """
        if click:
            mouse_pos = pygame.mouse.get_pos()
            
            #If click on "X" button, select X mode
            if self.easy_button.collidepoint(mouse_pos):
                self.selected_difficulty = "easy"
                self.on_config_menu = False
                self.on_titlescreen = True
            elif self.normal_button.collidepoint(mouse_pos):
                self.selected_difficulty = "normal"
                self.on_config_menu = False
                self.on_titlescreen = True
            elif self.hard_button.collidepoint(mouse_pos):
                self.selected_difficulty = "hard"
                self.on_config_menu = False
                self.on_titlescreen = True
                

    def titlescreen(self, click):
        """
        Display the title screen elements and handle user interaction.

        Args:
            click (bool): Indicates whether a mouse click event occurred.
        """
        self.screen.fill("black")
        self.screen.blit(self.game_title_image, self.game_title_rect)
        self.screen.blit(self.play_button_image, self.play_button_rect)
        self.screen.blit(self.config_button_image, self.config_button_rect)
    
        self.handle_titlescreen_events(click)
        

    def config_menu(self, click):
        """
        Renders text prompts for selecting difficulty levels and handle user user interaction.

        Args:
            click (bool): Indicates whether a mouse click event occurred.
        """
        self.screen.fill("black")
        draw_text("Selecione a dificuldade.", FONT, "white", self.screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 4)
        pygame.draw.rect(self.screen, "white", self.easy_button)
        draw_text("Fácil", FONT, "black", self.screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 25)
        pygame.draw.rect(self.screen, "white", self.normal_button)
        draw_text("Normal", FONT, "black", self.screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 95)
        pygame.draw.rect(self.screen, "white", self.hard_button)
        draw_text("Difícil", FONT, "black", self.screen, SCREEN_DIMENSIONS[0] // 2, SCREEN_DIMENSIONS[1] // 2 + 165)
        self.handle_config_menu_events(click)
        

    def update(self, click=False):
        """
        Update the game state based on the current screen phase.

        Args:
            click (bool, optional): Indicates whether a mouse click event occurred. Defaults to False.
        """
        if self.on_titlescreen:
            self.titlescreen(click)
        elif self.on_config_menu:
            self.config_menu(click)

    