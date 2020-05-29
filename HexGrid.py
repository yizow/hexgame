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
