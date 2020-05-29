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
        return [self.calc_corner(self.radius, degree)
                for degree in range(0, 360, 60)]

    def calc_corner(self, radius, angle):
        return tuple(map(round, (self.q + radius * math.cos(math.radians(angle)),
                                 self.r + radius * math.sin(math.radians(angle)))))


class HexMap:
    """Purely mathematical representation of a map of hexagons

    This class only deals with a hex map as discrete tiles. This includes
    operations like finding neighbors, pathfinding, grid based manipulation,
    etc.  Axial coordinates are used. All inputs and outputs should be (q, r)
    tuple grid coordinates.

    This class does NOT deal anything with pixels, drawing graphics, or the
    like.

    """

    directions = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]

    def __init__(self, width=0, height=0, should_wrap=True):
        """
        Wrapping behavior is controlled by two things:
            1) should_wrap
            2) width/height == 0
        These result in three modes when calling wrap() on negative/overflow indices:
            1) wrap: should_wrap == True and width/height > 0
            2) clamp: should_wrap == False and width/height > 0
            3) infinite: width/height <= 0

        Width and heigh have independent modes.

        Args:
            width (int):
            height (int):
            should_wrap (bool):

        """

        self.width = width
        self.height = height
        self.should_wrap = should_wrap

    def __iter__(self):
        if self.width > 0 and self.height > 0:
            for q in range(self.width):
                for r in range(self.height):
                    yield self[q, r]
        else:
            return "Attempting to iterate an infinite map"

    def wrap(self, q, r):
        """Return modified (q,r) based on wrapping rules.

        Return wrapped (q,r) if wrapping enabled and width/height > 0
        Return clamped (q,r) if wrapping disabled and width/height > 0
        Return unmodified otherwise

        """
        return self.wrap_single(
            q, self.width), self.wrap_single(r, self.height)

    def wrap_single(self, x, cap):
        """Wrap on a single axis"""
        if self.should_wrap:
            if cap > 0:
                x %= cap
        else:
            if cap > 0:
                x = 0 if x < 0 else cap if x > cap else x
        return x

    def get_neighbors(self, q, r, distance=1):
        """
        wrap/infinite: Return all neighbors.
        clamp: Return only unclamped neighbors.

        """
        neighbors = []
        for x, y in [(q + distance * x, r + distance * y)
                     for x, y in self.directions]:
            wrapped = self.wrap(x, y)
            if self.should_wrap or wrapped == (x, y):
                neighbors.append(wrapped)
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


a = HexMap()
