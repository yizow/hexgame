import os
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class HexTile:
    """Represents a single tile"""

    def __init__(self, radius, *center):
        self.radius = radius
        self.center = center

    @property
    def center(self):
        return (self.x, self.y, self.z)

    @center.setter
    def center(self, center):
        num_args = len(center)
        if num_args == 2:
            self.x, self.y = center
            self.z = 0 - self.x - self.y
        elif num_args == 3:
            self.x, self.y, self.z = center
        else:
            raise TypeError("Wrong number of arugment for HexTile center")

    @property
    def corners(self):
        return [self.calc_corner(self.radius, degree) for degree in range(0, 360, 60)]

    def calc_corner(self, radius, angle):
        return tuple(map(round, (self.x + radius * math.cos(math.radians(angle)), self.y + radius * math.sin(math.radians(angle)))))


class HexMap:
    def __init__(self, width=15, height=9, tile_radius=50):
        self.width = width
        self.height = height
        self.tile_radius = tile_radius

        self.tile_spacing_horiz = type(
            self).calc_tile_spacing_horiz(self.tile_radius)
        self.tile_spacing_vert = type(
            self).calc_tile_spacing_vert(self.tile_radius)

        self.map = []
        for x in range(width):
            row = []
            for y in range(height):
                center_x = x * self.tile_spacing_horiz
                center_y = y * self.tile_spacing_vert
                if x % 2:
                    center_y += self.tile_spacing_vert * .5
                # negative coordinates get cut off
                border_offset = 1 * self.tile_radius
                row.append(HexTile(self.tile_radius, border_offset +
                                   center_x, border_offset + center_y))
            self.map.append(row)

    def __getitem__(self, pos):
        x, y = pos
        return self.map[x][y]

    def __setitem__(self, pos, tile):
        x, y = pos
        self.map[x][y] = tile

    def __delitem__(self, pos):
        raise TypeError("Cannot delete tile from map")

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield self[x, y]

    def calc_tile_spacing_horiz(radius):
        return radius * 1.5

    def calc_tile_spacing_vert(radius):
        return radius * math.sqrt(3)
