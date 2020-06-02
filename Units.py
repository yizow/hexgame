import os
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

import constants


class Unit:
    """Represents a Unit

    A Unit returns information about how to render itself on a surface
    """

    def __init__(self, color=constants.WHITE):
        self.color = color

    def draw_unit(self, surface):
        raise NotImplemented


class Circle(Unit):
    """Represents a Unit as a Circle

    """

    def __init__(self, color=constants.BLUE, radius=3):
        super().__init__(color)

        self.radius = radius

    def draw_unit(self, surface, center):
        return pygame.draw.circle(surface, self.color, center, self.radius)


class Triangle(Unit):
    """ Represents a Unit as a Triangle

    """

    def __init__(self, color=constants.GREEN, size=10):
        """
        Args:
            size (int): Side length in pixels
        """
        super().__init__(color)

        self.size = size

    def get_corners(self, center):
        x, y = center
        return [(x + self.size / 2, y + self.size / 2 / math.sqrt(3)),
                (x - self.size / 2, y + self.size / 2 / math.sqrt(3)),
                (x, y - self.size / 2 / math.sqrt(3))]

    def draw_unit(self, surface, center):
        return pygame.draw.polygon(surface, self.color, self.get_corners(center))
