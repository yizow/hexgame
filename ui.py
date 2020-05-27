import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import HexMap

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

COLOR = (255, 0, 0)
RADIUS = 50
BORDER_BUFFER = 2


def main():
    pygame.display.quit()
    pygame.display.init()

    main_display = pygame.display.set_mode(
        size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
    num_tiles_width = int((SCREEN_WIDTH - BORDER_BUFFER * RADIUS) /
                          HexMap.HexMap.calc_tile_spacing_horiz(RADIUS))
    num_tiles_height = int((SCREEN_HEIGHT - BORDER_BUFFER * RADIUS) /
                           HexMap.HexMap.calc_tile_spacing_vert(RADIUS))
    for tile in HexMap.HexMap(num_tiles_width, num_tiles_height, RADIUS):
        pygame.draw.polygon(main_display, COLOR, tile.corners, 1)

    pygame.display.update()
