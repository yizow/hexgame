import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

import HexGrid
import Units


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

RADIUS = 50


def main():
    pygame.display.quit()
    pygame.display.init()

    main_display = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=DOUBLEBUF)

    hexgrid = HexGrid.HexGrid(main_display, radius=RADIUS)

    for tile in hexgrid:
        tile.draw_tile()

    pygame.display.update()

    running = True
    while running:
        event = pygame.event.wait()
        mouse_pos = pygame.mouse.get_pos()
        hovered_tile = hexgrid.hovered_tile(mouse_pos)
        updated_rects = None

        if event.type == QUIT:
            running = False
            break

        if event.type == KEYUP:
            if event.key == K_q:
                running = False
                break

            if event.key == K_c:
                if hovered_tile:
                    updated_rects = hovered_tile.add_unit(Units.Circle())

            elif event.key == K_t:
                if hovered_tile:
                    updated_rects = hovered_tile.add_unit(Units.Triangle())

            elif event.key == K_d:
                if hovered_tile:
                    updated_rects = hovered_tile.delete_unit()

        elif event.type == MOUSEMOTION:
            if hovered_tile:
                updated_rects = hexgrid.highlight_neighbors(hovered_tile, distance=2)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                main_display.fill((0, 0, 0))
            for tile in hexgrid:
                tile.draw_tile()
            hexgrid.previous_selected = None

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

        if updated_rects is not None:
            pygame.display.update(updated_rects)

    pygame.quit()


if __name__ == '__main__':
    main()
