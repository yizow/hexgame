import os
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

import constants
import HexMap

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

RADIUS = 50
BUFFER = 50


class HexTile:
    """Represents a single hex tile

    Tied to a HexGrid object. Tracks this tile's center, and calculates
    corners on demand for the purposes of drawing.

    """

    def __init__(self, hexgrid, radius, *center):
        self.hexgrid = hexgrid
        self.radius = radius
        self.center = center
        import random
        self.my_color = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))

    @property
    def inradius(self):
        return math.sqrt(3) * self.radius / 2

    @property
    def center(self):
        return (self.q, self.r)

    @center.setter
    def center(self, center):
        num_args = len(center)
        if num_args == 2:
            self.q, self.r = center
        else:
            raise TypeError("Wrong number of arugment for HexTile center")

    @property
    def corners(self):
        return [self.calc_corner(self.radius, degree)
                for degree in range(0, 360, 60)]

    def calc_corner(self, radius, angle):
        return tuple(map(round, (self.q + radius * math.cos(math.radians(angle)),
                                 self.r + radius * math.sin(math.radians(angle)))))

    def draw_tile(self):
        # return pygame.draw.polygon(self.hexgrid.surface, constants.RED, self.corners, 1)
        return pygame.draw.polygon(self.hexgrid.surface, self.my_color, self.corners, 1)

    def highlight_tile(self):
        return pygame.draw.polygon(self.hexgrid.surface, constants.WHITE, self.corners, 1)

    def __repr__(self):
        return "HexTile at: {}".format(self.center)


class HexGrid:
    """Displays a HexMap onto a pygame.Surface

    This class handles the translations between pixels and a HexMap. All UI
    functions are handled by this class.

    Inidividual tiles can be accessed by indexing: hexgrid[1, 2].
    An index can be accessed by indexing with a HexTile: hexgrid[hextile]

    """

    def __init__(self, surface, radius=50, should_wrap=False):
        """
        Args:
            surface (pygame.Surface):
            radius (int): Pixels between center and vertex of hexagon

        """
        self.surface = surface
        self.radius = radius
        self.inradius = HexTile(self, self.radius, 0, 0).inradius

        self.width = type(self).calc_num_columns(self.surface.get_width(), self.radius)
        self.x_offset = (self.surface.get_width() - self.width_used()) // 2

        self.height = type(self).calc_num_rows(self.surface.get_height(), self.inradius)
        self.y_offset = (self.surface.get_height() - self.height_used()) // 2

        self.tiles = []
        self.indices = {}
        for col in range(self.width):
            column = []
            for tile in range(self.height):
                center_q = self.x_offset + self.radius * (1.5 * col + 1)
                center_r = self.y_offset + self.inradius * (2 * tile + 1)
                if col % 2:
                    center_r += self.inradius
                column.append(HexTile(self, self.radius, round(center_q), round(center_r)))
                self.indices[column[-1]] = (col, tile)
            self.tiles.append(column)

        self.hexmap = HexMap.HexMap(self.width, self.height, should_wrap=should_wrap)

    def __getitem__(self, pos):
        if isinstance(pos, HexTile):
            return self.get_index(pos)
        q, r = pos
        return self.tiles[q][r]

    def __setitem__(self, pos, tile):
        q, r = pos
        self.tiles[q][r] = tile

    def __delitem__(self, pos):
        raise TypeError("Cannot delete HexTile from HexGrid")

    def __iter__(self):
        for r in range(self.height):
            for q in range(self.width):
                yield self[q, r]

    def get_index(self, tile):
        return self.indices[tile]

    def hovered_tile(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        mouse_x -= self.x_offset + self.radius
        mouse_y -= self.y_offset + self.inradius
        q = 2 * mouse_x / math.sqrt(3) / 2 / self.inradius
        r = (mouse_y - mouse_x / math.sqrt(3)) / (2 * self.inradius)
        q, r = type(self).hex_round(q, r)
        r += q // 2
        if q < 0 or r < 0:
            return None
        try:
            return self[q, r]
        except IndexError:
            return None

    def hex_round(q, r):
        x, y, z = q, r, -q - r

        rounded_x, rounded_y, rounded_z = map(round, (x, y, z))

        x_delta, y_delta, z_delta = map(
            abs, (x - rounded_x, y - rounded_y, z - rounded_z))

        if x_delta > y_delta and x_delta > z_delta:
            rounded_x = -rounded_y - rounded_z
        elif y_delta > z_delta:
            rounded_y = -rounded_x - rounded_z
        else:
            rounded_z = -rounded_x - rounded_y

        return rounded_x, rounded_y

    def width_used(self):
        return round(self.radius * (3 * self.width + 1) // 2)

    def height_used(self):
        return round(self.inradius * (self.height * 2 + 1))

    def calc_num_columns(width, radius):
        return int((2 * width - radius) // (3 * radius))

    def calc_num_rows(height, inradius):
        return int((height - inradius) // (2 * inradius))

    def highlight_neighbors(self, tile, distance=1):
        neighbors = self.hexmap.get_neighbors(*self[tile], distance)
        for tile in [self[index] for index in neighbors]:
            tile.highlight_tile()


def main():
    pygame.display.quit()
    pygame.display.init()

    main_display = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)

    hexgrid = HexGrid(main_display, radius=200)

    for tile in hexgrid:
        tile.draw_tile()

    for tile in hexgrid:
        pygame.draw.circle(main_display, constants.BLUE, tile.center, 2)

    pygame.display.update()

    running = True
    while running:
        event = pygame.event.wait()

        if event.type == QUIT:
            running = False
            break

        elif event.type == MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            hovered_tile = hexgrid.hovered_tile(mouse_pos)
            if hovered_tile:
                hexgrid.highlight_neighbors(hovered_tile)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                main_display.fill((0, 0, 0))
            for tile in hexgrid:
                tile.draw_tile()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                continue
            print("executing map")
            for x in range(main_display.get_width()):
                for y in range(main_display.get_height()):
                    hovered_tile = hexgrid.hovered_tile((x, y))
                    if hovered_tile:
                        color = hovered_tile.my_color
                        main_display.set_at((x, y), color)

        pygame.display.update()

    pygame.quit()
