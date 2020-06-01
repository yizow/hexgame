import unittest
import logging
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import HexMap
from HexGrid import HexGrid


class TestHexMap(unittest.TestCase):

    def test_get_neighbors_infinite(self):
        hexmap = HexMap.HexMap(0, 0, False)
        expected = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_clamp(self):
        hexmap = HexMap.HexMap(3, 3, False)
        expected = [(1, 0), (0, 1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_wrap(self):
        hexmap = HexMap.HexMap(3, 3, True)
        expected = [(1, 2), (1, 0), (0, 1), (2, 1), (2, 0), (0, 2)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_clamp_horiz_infinite_vert(self):
        hexmap = HexMap.HexMap(3, 0, False)
        expected = [(1, -1), (1, 0), (0, 1), (0, -1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))

    def test_get_neighbors_distance(self):
        hexmap = HexMap.HexMap(0, 0, False)
        expected = [(2, -2), (2, 0), (0, 2), (-2, 2), (-2, 0), (0, -2)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0, 2))

    def test_get_neighbors_infinite_wrap(self):
        hexmap = HexMap.HexMap(0, 0, True)
        expected = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        self.assertEqual(expected, hexmap.get_neighbors(0, 0))


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
        self.assertEqual(87, hexgrid.height_used())

    def test_calc_num_columns(self):
        self.assertEqual(2, HexGrid.calc_num_columns(9, 2))
        self.assertEqual(3, HexGrid.calc_num_columns(10, 2))
        self.assertEqual(3, HexGrid.calc_num_columns(12, 2))
        self.assertEqual(4, HexGrid.calc_num_columns(13, 2))

    def test_calc_num_rows(self):
        self.assertEqual(1, HexGrid.calc_num_rows(2, 1))
        self.assertEqual(2, HexGrid.calc_num_rows(3, 1))
        self.assertEqual(3, HexGrid.calc_num_rows(4, 1))

    def test_init(self):
        hexgrid = HexGrid(self.surface, radius=20)
        self.assertEqual(3, hexgrid.width)
        self.assertEqual(1, hexgrid.height)

        expected_centers = [(20, 50), (50, 84), (80, 50)]

        centers = [hexgrid[col, row].center for row in range(hexgrid.height) for col in range(hexgrid.width)]
        self.assertEqual(expected_centers, centers)

        self.assertEqual(expected_centers, [tile.center for tile in hexgrid])

    def test_hovered_tile(self):
        hexgrid = HexGrid(self.surface, radius=20)
        self.assertEqual(hexgrid[0, 0], hexgrid.hovered_tile((20, 50)))
        self.assertEqual(hexgrid[1, 0], hexgrid.hovered_tile((50, 50)))
        self.assertEqual(hexgrid[2, 0], hexgrid.hovered_tile((80, 50)))



if __name__ == '__main__':
    log = logging.getLogger()
    log.level = logging.DEBUG
    unittest.main()
