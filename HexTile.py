import os
import sys
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

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
    return (self.x + radius * math.cos(math.radians(angle)), self.y + radius * math.sin(math.radians(angle)))


class HexMap:
  def __init__(self, width=15, height=9, tile_radius=50):
    self.width = width
    self.height = height
    self.tile_radius = tile_radius

    self.map = []
    for x in range(width):
      row = []
      for y in range(height):
        center_x = x * self.tile_radius * 1.5
        center_y = y * self.tile_radius * math.sqrt(3)
        if x % 2:
          center_y += self.tile_radius * math.sqrt(3) * .5
        row.append(HexTile(self.tile_radius, 2 * self.tile_radius + center_x, 2 * self.tile_radius + center_y))
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


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

COLOR = (255, 0, 0)
RADIUS = 50
BORDER_BUFFER = 2

def main():
  pygame.display.quit()
  pygame.display.init()

  main_display = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
  num_tiles_width = int((SCREEN_WIDTH - BORDER_BUFFER * RADIUS) / (1.5 * RADIUS))
  num_tiles_height = int((SCREEN_HEIGHT - BORDER_BUFFER * RADIUS) / (math.sqrt(3) * RADIUS))
  for tile in HexMap(num_tiles_width, num_tiles_height, RADIUS):
    pygame.draw.polygon(main_display, COLOR, tile.corners, 1)

  pygame.display.update()
