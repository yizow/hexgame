import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

import constants
import HexMap

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

RADIUS = 50
TILE_BUFFER = 1
BUFFER = 50

display = None


class HexTile:
    """Represents a single hex tile

    Tied to a HexGrid objects. Tracks this tile's center, and calculates
    corners on demand for the purposes of drawing.

    """

    def __init__(self, radius, *center):
        self.radius = radius
        self.center = center

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


class HexGrid:
    """Displays a HexMap onto a screen

    This class handles the translations between pixels and a HexMap. All UI
    functions are handled by this class.

    """

    def hovered_tile(self, mouse_pos):
        mouse_x, mouse_y = map(lambda x: x + self.border_offset, mouse_pos)
        q = 2. / 3 * mouse_x / self.tile_radius
        r = (-1. / 3 * mouse_x + math.sqrt(3) / 3 * mouse_y) / self.tile_radius
        return type(self).hex_round(q, r)

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


def highlight_tile(tile):
    return pygame.draw.polygon(display, WHITE, tile.corners, 1)


def highlight_neighbors(hexmap, q, r):
    print("highlight_neighbors", q, r)
    neighbors = [highlight_tile(neighbor)
                 for neighbor in hexmap.get_neighbors(q, r, distance=2)]
    return neighbors[0].unionall(neighbors)


def main():
    global display
    pygame.display.quit()
    pygame.display.init()

    main_display = pygame.display.set_mode(
        size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
    grid = pygame.Surface(
        (SCREEN_WIDTH - 2 * BUFFER, SCREEN_HEIGHT - 2 * BUFFER))

    display = grid

    screen_width = display.get_width()
    screen_height = display.get_height()
    num_tiles_width = int((screen_width - TILE_BUFFER * RADIUS) /
                          HexMap.HexMap.calc_tile_spacing_horiz(RADIUS))
    num_tiles_height = int((screen_height - TILE_BUFFER * RADIUS) /
                           HexMap.HexMap.calc_tile_spacing_vert(RADIUS))

    hexmap = HexMap.HexMap(num_tiles_width, num_tiles_height, RADIUS)
    for tile in hexmap:
        pygame.draw.polygon(display, RED, tile.corners, 1)

    if display == grid:
        main_display.blit(grid, (BUFFER, BUFFER))

    pygame.display.update()

    running = True
    while running:
        event = pygame.event.wait()

        if event.type == QUIT:
            running = False
            break

        if event.type == MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            grid_mouse_pos = (mouse_pos[0] - BUFFER, mouse_pos[1] - BUFFER)
            hovered_tile = hexmap.hovered_tile(grid_mouse_pos)
            updated_rect = highlight_neighbors(hexmap, *hovered_tile)
            #main_display.blit(grid, updated_rect)

        # pygame.display.update()

    pygame.quit()