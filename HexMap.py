import os
import math


class HexMap:
    """Purely mathematical representation of a map of hexagons

    This class only deals with a hex map as discrete tiles. This includes operations like finding neighbors,
    pathfinding, grid based manipulation, etc. Axial coordinates are used. All inputs and outputs should be
    (q, r) tuple grid coordinates.

    This class does NOT deal anything with pixels, drawing graphics, or the like.

    Using odd-q offset coordinates; all odd columns shifted vertically

    """

    cube_directions = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1)]
    directions = [[(1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1)],
                  [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (0, -1)]]

    def __init__(self, width=0, height=0, should_wrap=False):
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

    def wrap(self, q, r):
        """Return modified (q,r) based on wrapping rules.

        Return wrapped (q,r) if wrapping enabled and width/height > 0
        Return clamped (q,r) if wrapping disabled and width/height > 0
        Return unmodified otherwise

        """
        return self.wrap_single(q, self.width), self.wrap_single(r, self.height)

    def wrap_single(self, x, cap):
        """Wrap on a single axis"""
        if self.should_wrap:
            if cap > 0:
                x %= cap
        else:
            if cap > 0:
                x = 0 if x < 0 else ((cap - 1) if x >= cap else x)
        return x

    def cube_to_offset(x, y, z):
        return (x, y + (x - (x & 1)) // 2)

    def offset_to_cube(q, r):
        x = q
        y = r - (q - (q & 1)) // 2
        z = -x - y
        return (x, y, z)

    def get_neighbors(self, q, r, distance=1):
        """
        wrap/infinite: Return all neighbors.
        clamp: Return only unclamped neighbors.

        """
        neighbors = []
        for direction in self.cube_directions:
            scaled_direction = [distance * coord for coord in direction]
            cube_coordinates = type(self).offset_to_cube(q, r)
            neighbor = [sum(coord) for coord in zip(scaled_direction, cube_coordinates)]
            neighbor = type(self).cube_to_offset(*neighbor)
            wrapped = self.wrap(*neighbor)

            if self.should_wrap or wrapped == neighbor:
                neighbors.append(wrapped)
        return neighbors
