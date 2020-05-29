import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import HexMap

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

COLOR = (255, 0, 0)
RADIUS = 50
TILE_BUFFER = 1
BUFFER = 50


def main():
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

    for tile in HexMap.HexMap(num_tiles_width, num_tiles_height, RADIUS):
        pygame.draw.polygon(display, COLOR, tile.corners, 1)

    if display == grid:
        main_display.blit(grid, (BUFFER, BUFFER))

    pygame.display.update()
