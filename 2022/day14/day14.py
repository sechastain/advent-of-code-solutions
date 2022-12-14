
import re
import sys
import json

from ..utils.io import readlines
from functools import reduce, cmp_to_key

class Board:
  def __init__(self):
    self.occupied = set()
    self.sand = 0

  def _add_interpolated_points(self, p1, p2):
    xy = 1 if p1[0] == p2[0] else 0
    dir = 1 if p1[xy] < p2[xy] else -1
    pt = list(p1)
    while pt[xy] != p2[xy]:
      self.occupied.add(tuple(pt))
      pt[xy] += dir

  def add_line(self, points):
    for i in range(len(points)-1):
      self._add_interpolated_points(*points[i:i+2])

    self.occupied.add(tuple(points[-1]))

  def determine_max_depth(self):
    self.max = max([p[1] for p in self.occupied])

  def drop_sand(self, intoInfinity=True):
    fromPt = (500,0)
    while True:
      candidates = [(fromPt[0] + i, fromPt[1]+1) for i in range(-1,2)]
      if intoInfinity and candidates[0][1] > self.max:
        return False 
      elif not intoInfinity and candidates[0][1] == self.max+2:
        self.occupied.add(fromPt)
        self.sand += 1
        return True
      elif candidates[1] not in self.occupied:
        fromPt = candidates[1]
      elif candidates[0] not in self.occupied:
        fromPt = candidates[0]
      elif candidates[2] not in self.occupied:
        fromPt = candidates[2]
      else:
        self.occupied.add(fromPt)
        self.sand += 1
        return True

def parseLine(board, line):
  points = [p for p in line.split(' ') if p != '->']
  points = [[int(coord) for coord in p.split(',')] for p in points]
  board.add_line(points)

  return board

board = readlines(sys.argv[1], parseLine, Board())
board.determine_max_depth()
while board.drop_sand():
  pass
print(board.sand)

board = readlines(sys.argv[1], parseLine, Board())
board.determine_max_depth()
while (500, 0) not in board.occupied:
  board.drop_sand(False)
  pass
print(board.sand)

