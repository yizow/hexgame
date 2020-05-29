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
        return [self.calc_corner(self.radius, degree) for degree in range(0, 360, 60)]

    def calc_corner(self, radius, angle):
        return tuple(map(round, (self.q + radius * math.cos(math.radians(angle)), self.r + radius * math.sin(math.radians(angle)))))


class HexMap:
    directions = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    def __init__(self, width=15, height=9, tile_radius=50):
        self.width = width
        self.height = height
        self.tile_radius = tile_radius
        self.border_offset = 1 * self.tile_radius

        self.tile_spacing_horiz = type(
            self).calc_tile_spacing_horiz(self.tile_radius)
        self.tile_spacing_vert = type(
            self).calc_tile_spacing_vert(self.tile_radius)

        self.map = []
        for q in range(width):
            row = []
            for r in range(height):
                center_q = q * self.tile_spacing_horiz
                center_r = r * self.tile_spacing_vert
                if q % 2:
                    center_r += self.tile_spacing_vert * .5
                # negative coordinates get cut off
                row.append(HexTile(self.tile_radius, self.border_offset +
                                   center_q, self.border_offset + center_r))
            self.map.append(row)

    def __getitem__(self, pos):
        q, r = pos
        return self.map[q][r]

    def __setitem__(self, pos, tile):
        q, r = pos
        self.map[q][r] = tile

    def __delitem__(self, pos):
        raise TypeError("Cannot delete tile from map")

    def __iter__(self):
        for q in range(self.width):
            for r in range(self.height):
                yield self[q, r]

    def calc_tile_spacing_horiz(radius):
        return radius * 1.5

    def calc_tile_spacing_vert(radius):
        return radius * math.sqrt(3)

    def get_neighbors(self, q, r, distance=1):
        neighbors = []
        print("get_neighbors", [(distance * q, distance * r) for q, r in self.directions])
        for q_delta, r_delta in [(distance * q, distance * r) for q, r in self.directions]:
            neighbors.append(self[(q + q_delta) %
                                  self.width, (r + r_delta) % self.height])
        return neighbors

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
