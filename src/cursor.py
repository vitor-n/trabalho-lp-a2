import pygame
from utils import load_image
import math

class Cursor:
    """
    This class represents the cursor object in the game.
    """

    def __init__(self, image_path: str, initial_position: tuple, player: object):
        """
        Args:
            image_path (str): Path to the image file for the cursor.
            initial_position (tuple): Initial position of the cursor.
            player (object): Reference to the player object.
        """
        self._player = player
        self._image = load_image(image_path)
        self._rect = self._image.get_rect(center=initial_position)
        self._angle_radians = 0
        self._angle_degrees = 0

    @property
    def image(self) -> pygame.Surface:
        """
        Returns the pygame Surface object of the cursor image.
        """
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        """
        Returns the pygame Rect object of the cursor's position and size.
        """
        return self._rect

    @property
    def angle_radians(self) -> float:
        """
        Returns the angle of the cursor in radians.
        """
        return self._angle_radians

    @property
    def angle_degrees(self) -> float:
        """
        Returns the angle of the cursor in degrees.
        """
        return self._angle_degrees

    def set_camera(self, camera: object):
        """
        Sets the camera object for the cursor.

        Args:
            camera (object): Reference to the camera object.
        """
        self._camera = camera

    def update(self):
        """
        Updates the position and angle of the cursor based on the player's position and the mouse position.
        """
        player_position_screen_space = self._camera.calculate_offset(self._player.rect)

        self._rect.center = pygame.mouse.get_pos()
        self._angle_radians = math.atan2(
            player_position_screen_space[1] - self._rect.centery,
            self._rect.centerx - player_position_screen_space[0],
        )
        self._angle_degrees = math.degrees(self._angle_radians)
