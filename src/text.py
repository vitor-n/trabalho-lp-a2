
import pygame
from utils import load_image, image_clip
from settings import PX_SCALE

class Font():
    def __init__(self, image_path):
        font_image = load_image(image_path)

        self.character_order = "abcdefghijklmnopqrstuvwxyz0123456789,.?!:/\<>"
        
        self.characters = {}
        character_count = 0
        current_character_width = 0
        separator_counter = 1

        for pixel_x in range(font_image.get_width()):
            color = font_image.get_at((pixel_x, 0))
            if separator_counter == 1:
                if color == (255,0,255):
                    character_image = image_clip(font_image, pixel_x - current_character_width, 0, current_character_width, font_image.get_height())
                    self.characters[self.character_order[character_count]] = character_image.copy()
                    character_count += 1
                    current_character_width = 0
                    pixel_x += 0
                    separator_counter = PX_SCALE
                else:
                    current_character_width += 1
            else:
                separator_counter -= 1

    def render(self, surface, text, position):
        x_offset = 0
        text = text.lower()
        for character in text:
            if character != " ":
                surface.blit(self.characters[character], (position[0] + x_offset, position[1]))
                x_offset += self.characters[character].get_width() + 3
            else:
                x_offset += 10
