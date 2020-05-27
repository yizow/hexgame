import os
import sys
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

class HexTile:
  """Represents a single tile"""

  def __init__(self, *center):
    self.set_center(*center);

  def set_center(self, *center):
    num_args = len(center)
    if num_args == 2:
      self.x, self.y = center
      self.z = 0 - self.x - self.y
    elif num_args == 3:
      self.x, self.y, self.z = center
    else:
      raise TypeError("Wrong number of arugment for HexTile center")

  def get_corners(self, radius):
    return [self.calc_corner(radius, degree) for degree in range(0, 360, 60)]

  def calc_corner(self, radius, angle):
    return (self.x + radius * math.cos(math.radians(angle)), self.y + radius * math.sin(math.radians(angle)))


class HexMap:
  def __init__(self, width=25, height=10, tile_radius=50):
    self.width = width
    self.height = height
    self.tile_radius = tile_radius

    self.map = []
    for x in range(width):
      row = []
      for y in range(height):
        center_x = x * tile_radius * 1.5
        center_y = y * tile_radius * math.sqrt(3)
        if x % 2:
          center_y += tile_radius * math.sqrt(3) * .5
        row.append(HexTile(center_x, center_y))
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


def main():
  pygame.display.quit()
  pygame.display.init()
  main_display = pygame.display.set_mode(size=(1600,900), flags=pygame.RESIZABLE)
  for tile in HexMap():
    pygame.draw.polygon(main_display, (255, 0, 0), tile.get_corners(50), 1)

  pygame.display.update()
