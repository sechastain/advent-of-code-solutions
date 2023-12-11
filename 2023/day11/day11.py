
import sys
import re

from functools import reduce
from collections import namedtuple

Node = namedtuple('Node', ['left', 'right'])

def stripListReduce(alist, astr):
  return alist + [list(astr.strip())] 

def readlines(file, reduceFn = stripListReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def findGalaxies(amap):
  galaxies = []
  for row in range(len(amap)):
    for col in range(len(amap[row])):
      cell = amap[row][col]
      if cell != '.':
        galaxies += [(row, col, cell)]
  
  return galaxies

def expandRows(amap, galaxies):
  rows = list(range(len(amap)))
  galaxies = [g[0] for g in galaxies]
  for g in galaxies:
    if g in rows:
      rows.remove(g)

  return rows

def expandCols(amap, galaxies):
  cols = list(range(len(amap[0])))
  galaxies = [g[1] for g in galaxies]
  for g in galaxies:
    if g in cols:
      cols.remove(g)

  return cols

def findClosestNeighbors(amap, galaxies, emptyWeight=2):
  dist = 0
  emptyRows = expandRows(amap, galaxies)
  emptyCols = expandCols(amap, galaxies)
  process = galaxies[:]
  search = galaxies[:]
  for g in galaxies:
    search.remove(g)
    for s in search:
      r1, c1, _ = g
      r2, c2, _ = s
      r1, r2 = (r1, r2) if r1 < r2 else (r2, r1)
      c1, c2 = (c1, c2) if c1 < c2 else (c2, c1)
      r = r2 - r1
      c = c2 - c1
      dist += r + c \
        + len([er for er in emptyRows if er > r1 and er < r2]) * (emptyWeight-1)  \
        + len([ec for ec in emptyCols if ec > c1 and ec < c2]) * (emptyWeight-1) 

  return dist

amap = readlines(sys.argv[1])
galaxies = findGalaxies(amap)
print(findClosestNeighbors(amap, galaxies))
print(findClosestNeighbors(amap, galaxies, 10))
print(findClosestNeighbors(amap, galaxies, 100))
print(findClosestNeighbors(amap, galaxies, 1000000))


