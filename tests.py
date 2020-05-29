import unittest
import logging
import sys

import HexMap


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


if __name__ == '__main__':
    log = logging.getLogger()
    log.level = logging.DEBUG
    unittest.main()
