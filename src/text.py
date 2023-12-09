import pygame
from utils import load_image, image_clip
from settings import PX_SCALE


class Font:
    """
    This class represents a custom font loaded from an image file.
    """

    def __init__(self, image_path: str):
        """
        Loads the font image and constructs a dictionary mapping characters to their corresponding image surfaces.

        Args:
            image_path (str): Path to the font image file.
        """

        self.character_order = "abcdefghijklmnopqrstuvwxyz0123456789,.?!:/\<>()-="
        self.characters = {}
        
        font_image = load_image(image_path)
        character_count = 0
        current_character_width = 0
        separator_counter = 1

        # Iterate over each pixel in the font image
        for pixel_x in range(font_image.get_width()):
            color = font_image.get_at((pixel_x, 0))

            # Check if the pixel marks the beginning of a new character
            if separator_counter == 1:
                if color == (255, 0, 255):
                    # Extract the character image and store it in the dictionary
                    character_image = image_clip(
                        font_image,
                        pixel_x - current_character_width,
                        0,
                        current_character_width,
                        font_image.get_height(),
                    )
                    self.characters[self.character_order[character_count]] = character_image.copy()
                    character_count += 1
                    current_character_width = 0
                    pixel_x += 0  # Skip the separator pixel
                    separator_counter = PX_SCALE
                else:
                    current_character_width += 1  # Accumulate pixel width for the current character
            else:
                separator_counter -= 1  # Count down the separator pixel length

    def render(self, surface: pygame.Surface, text: str, position: tuple):
        """
        Renders the given text onto the provided surface at the specified position.

        Args:
            surface (pygame.Surface): The surface to render the text on.
            text (str): The text to render.
            position (tuple): The position (x, y) to render the text at.
        """
        x_offset = 0
        text = text.lower()

        # Iterate over each character in the text
        for character in text:
            # Check if the character is a space
            if character != " ":
                # Blit the character image onto the surface with proper spacing
                surface.blit(self.characters[character], (position[0] + x_offset, position[1]))
                x_offset += self.characters[character].get_width() + 3
            else:
                # Apply space character spacing
                x_offset += 10
