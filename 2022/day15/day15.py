
import re
import sys
import json

from ..utils.io import readlines
from functools import reduce, cmp_to_key

def smoosh(alist, xrange):
  if len(alist) == 0:
    return [xrange]
  
  lxrange = alist[-1]
  if lxrange[1] >= xrange[0]:
    if lxrange[1] < xrange[1]:
      lxrange[1] = xrange[1]
  else:
    alist.append(xrange)

  return alist

def clip(bound):
  def _clip(alist, x):
    if x[0] < 0 and x[1] < 0:
      return alist
    elif x[0] > bound and x[1] > bound:
      return alist
    if x[0] < 0:
      x[0] = 0
    if x[1] > bound:
      x[1] = bound
    alist.append(x)
    return alist

  return _clip
    
class Board:
  def __init__(self):
    self.occupied = set()
    self.objs = dict()

  def _get_xrange(self, pt, y):
    ydist = abs(y - pt['sensor'][1])
    maxdist = pt['dist']
    xunits = (maxdist - ydist)
    x0 = pt['sensor'][0]
    return [x0 + x for x in [-xunits, xunits]]

  def _get_coverage(self, y):
    coverage = [p for p in self.objs.values() if y >= p['min_y'] and y <= p['max_y']]
    covered = [self._get_xrange(pt, y) for pt in coverage]
    covered.sort(key=lambda x: x[0])
    covered = reduce(smoosh, covered, [])
    return covered

  def _count_occupied(self, xranges, y):
    occ = [o for o in self.occupied if o[1] == y]
    hit = 0
    for o in occ:
      for xr in xranges:
        if o[0] >= xr[0] and o[0] <= xr[1]:
          hit += 1
    return hit
      
  def not_beacons(self, y):
    covered = self._get_coverage(y)
    clen = sum([x[1] - x[0] + 1 for x in covered])
    occ = self._count_occupied(covered, y)
    return clen - occ

  def find_uncovered_points(self, bound):
    for y in range(bound+1):
      covered = self._get_coverage(y)
      if len(covered) > 1:
        covered = reduce(clip(bound), covered, [])
        if len(covered) > 1:
          return covered[0][1] * bound + y
    return -1
    
  def add_coverage(self, p1, p2):
    self.occupied.add(p1)
    self.occupied.add(p2)
    dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
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

print(board.find_uncovered_points(20))
print(board.find_uncovered_points(4000000))

