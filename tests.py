import unittest
import logging
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import HexMap
from HexGrid import HexGrid


class TestHexMap(unittest.TestCase):

    def test_contains(self):
        hexmap = HexMap.HexMap(8, 8, False)
        self.assertEqual(True, hexmap.contains(0, 0))
        self.assertEqual(True, hexmap.contains(5, 5))
        self.assertEqual(False, hexmap.contains(10, 10))
        self.assertEqual(False, hexmap.contains(-5, -5))

    def test_contains_infinite(self):
        hexmap = HexMap.HexMap(0, 0, False)
        self.assertEqual(True, hexmap.contains(0, 0))
        self.assertEqual(True, hexmap.contains(5, 5))
        self.assertEqual(True, hexmap.contains(-5, -5))

    def test_get_neighbors_infinite(self):
        hexmap = HexMap.HexMap(0, 0, False)
        expected = [(1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_clamp(self):
        hexmap = HexMap.HexMap(3, 3, False)
        expected = [(1, 0), (0, 1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_clamp_horiz_infinite_vert(self):
        hexmap = HexMap.HexMap(3, 0, False)
        expected = [(1, -1), (1, 0), (0, 1), (0, -1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_distance(self):
        hexmap = HexMap.HexMap(0, 0, False)
        expected = [(2, -1), (2, 1), (0, 2), (-2, 1), (-2, -1), (0, -2)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0, 2))

    def test_get_neighbors_middle(self):
        hexmap = HexMap.HexMap(5, 2, False)
        expected = [(2, 0), (2, 1), (1, 1), (0, 1), (0, 0)]
        self.assertEqual(expected, hexmap.get_neighbors(1, 0))

    def test_ring_full(self):
        hexmap = HexMap.HexMap(10, 10, False)

        expected = [(3, 3), (4, 3), (5, 3), (5, 4), (4, 5), (3, 4)]
        self.assertEqual(expected, hexmap.get_ring(4, 4, 1))

        expected = [(2, 3), (3, 2), (4, 2), (5, 2), (6, 3), (6, 4),
                    (6, 5), (5, 5), (4, 6), (3, 5), (2, 5), (2, 4)]
        self.assertEqual(expected, hexmap.get_ring(4, 4, 2))

    def test_ring_clipped(self):
        hexmap = HexMap.HexMap(7, 5, False)

        expected = [(2, 3), (3, 2), (4, 2), (5, 2), (6, 3), (6, 4), (2, 4)]
        self.assertEqual(expected, hexmap.get_ring(4, 4, 2))


class TestHexGrid(unittest.TestCase):

    def setUp(self):
        self.surface = pygame.Surface((100, 100))

    def test_width_used(self):
        hexgrid = HexGrid(self.surface, radius=50)
        self.assertEqual(100, hexgrid.width_used())
        hexgrid = HexGrid(self.surface, radius=20)
        self.assertEqual(100, hexgrid.width_used())
        hexgrid = HexGrid(self.surface, radius=40)
        self.assertEqual(80, hexgrid.width_used())

    def test_height_used(self):
        hexgrid = HexGrid(self.surface, radius=10)
        self.assertEqual(95, hexgrid.height_used())

    def test_calc_num_columns(self):
        self.assertEqual(2, HexGrid.calc_num_columns(9, 2))
        self.assertEqual(3, HexGrid.calc_num_columns(10, 2))
        self.assertEqual(3, HexGrid.calc_num_columns(12, 2))
        self.assertEqual(4, HexGrid.calc_num_columns(13, 2))

    def test_calc_num_rows(self):
        self.assertEqual(1, HexGrid.calc_num_rows(3, 1))
        self.assertEqual(1, HexGrid.calc_num_rows(4, 1))
        self.assertEqual(2, HexGrid.calc_num_rows(5, 1))

    def test_init(self):
        hexgrid = HexGrid(self.surface, radius=20)
        self.assertEqual(3, hexgrid.width)
        self.assertEqual(2, hexgrid.height)

        expected_centers = [(20, 23), (50, 41), (80, 23),
                            (20, 58), (50, 75), (80, 58)]

        centers = [hexgrid[col, row].center for row in range(hexgrid.height) for col in range(hexgrid.width)]
        self.assertEqual(expected_centers, centers)

        self.assertEqual(expected_centers, [tile.center for tile in hexgrid])

    def test_hovered_tile(self):
        hexgrid = HexGrid(self.surface, radius=20)
        self.assertEqual(hexgrid[0, 0], hexgrid.hovered_tile((20, 23)))
        self.assertEqual(hexgrid[1, 0], hexgrid.hovered_tile((50, 41)))
        self.assertEqual(hexgrid[2, 0], hexgrid.hovered_tile((80, 23)))
        self.assertEqual(hexgrid[0, 1], hexgrid.hovered_tile((20, 58)))
        self.assertEqual(hexgrid[1, 1], hexgrid.hovered_tile((50, 75)))


if __name__ == '__main__':
    log = logging.getLogger()
    log.level = logging.DEBUG
    unittest.main()
