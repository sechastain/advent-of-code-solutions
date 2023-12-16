
import sys
import re

from collections import namedtuple
from functools import reduce

def stripReduce(alist, astr):
  return alist + [list(astr.strip())] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

Photon = namedtuple('Photon', ['row', 'col', 'rvel', 'cvel'])

def reflect(mirror, p):
  # reflect up
  if (mirror == '/' and p.cvel == 1) or \
     (mirror == '\\' and p.cvel == -1): 
    return [Photon(p.row - 1, p.col, -1, 0)]

  # reflect down
  if (mirror == '/' and p.cvel == -1) or \
     (mirror == '\\' and p.cvel == 1): 
    return [Photon(p.row + 1, p.col, 1, 0)]


  # reflect left
  if (mirror == '/' and p.rvel == 1) or \
     (mirror == '\\' and p.rvel == -1): 
    return [Photon(p.row, p.col - 1, 0, -1)]

  # reflect right
  if (mirror == '/' and p.rvel == -1) or \
     (mirror == '\\' and p.rvel == 1): 
    return [Photon(p.row, p.col + 1, 0, 1)]

def splitHor(mirror, p):
  if p.rvel == 0:
    return cont(mirror, p)
  return [
    Photon(p.row, p.col - 1, 0, -1),
    Photon(p.row, p.col + 1, 0, 1),
  ]

def splitVer(mirror, p):
  if p.cvel == 0:
    return cont(mirror, p)
  return [
    Photon(p.row - 1, p.col, -1, 0),
    Photon(p.row + 1, p.col, 1, 0),
  ]

def cont(space, p):
  row = p.row + p.rvel
  col = p.col + p.cvel
  return [Photon(row, col, p.rvel, p.cvel)]

nextMap = {
  '.': cont,
  '/': reflect,
  '\\': reflect,
  '|': splitVer,
  '-': splitHor,
}

def nextPos(amap, p):
  cur = amap[p.row][p.col]
  return nextMap[cur](cur, p)

def fillMap(amap, start=Photon(0, 0, 0, 1)):
  visited = set()
  tovisit = [start]
  while len(tovisit) > 0:
    p = tovisit.pop(0)
    if p not in visited and p.row >= 0 and p.col >= 0 and p.row < len(amap) and p.col < len(amap[p.row]):
      visited.add(p)
      tovisit.extend(nextPos(amap, p))
  return visited

def maxMap(amap):
  rows = len(amap)
  cols = len(amap[0])
  top = [Photon(0, c, 1, 0) for c in range(cols)]
  bottom = [Photon(rows-1, c, -1, 0) for c in range(cols)]
  left = [Photon(r, 0, 0, 1) for r in range(rows)]
  right = [Photon(r, cols-1, 0, -1) for r in range(rows)]
  
  tovisit = []
  tovisit.extend(top)
  tovisit.extend(bottom)
  tovisit.extend(left)
  tovisit.extend(right)

  def maxtest(max, p):
    visited = fillMap(amap, p)
    return max if countEnergized(max) > countEnergized(visited) else visited

  return reduce(maxtest, tovisit[1:], fillMap(amap, tovisit[0]))

def countEnergized(visited):
  return len(set((v.row, v.col) for v in visited))

amap = readlines(sys.argv[1])
print(countEnergized(fillMap(amap)))
print(countEnergized(maxMap(amap)))

