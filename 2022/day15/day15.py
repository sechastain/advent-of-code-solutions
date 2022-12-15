
import re
import sys
import json

from ..utils.io import readlines
from functools import reduce, cmp_to_key

class Board:
  def __init__(self):
    self.occupied = set()
    self.objs = dict()

  def _get_covered_points(self, pt, y):
    ydist = abs(y - pt['sensor'][1])
    maxdist = pt['dist']
    xunits = (maxdist - ydist)
    x0 = pt['sensor'][0]
    return [(x0 + x, y) for x in range(-xunits, xunits+1)]

  def not_beacons(self, y):
    coverage = [p for p in self.objs.values() if y >= p['min_y'] and y <= p['max_y']]
    covered = set()
    for pt in coverage:
      covered.update(self._get_covered_points(pt, y))
    covered = [c for c in covered if c not in self.occupied]
    return len(covered)

  def uncovered_points(self, bound):
    pass
    
  def add_coverage(self, p1, p2):
    self.occupied.add(p1)
    self.occupied.add(p2)
    dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    print('dist', dist)
    self.objs[p1] = {
      'sensor': p1,
      'beacon': p2,
      'dist': dist,
      'min_y': p1[1] - dist,
      'max_y': p1[1] + dist,
    }

def parseLine(board, line):
  points = line.split(':')
  intpt = lambda x: int(x.split('=')[1])
  points = [tuple([intpt(c) for c in  p.split(',')]) for p in line.split(':')]
  board.add_coverage(*points)

  return board

board = readlines(sys.argv[1], parseLine, Board())

print(board.not_beacons(10))
print(board.not_beacons(2000000))
