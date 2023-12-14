
import sys
import re

from functools import reduce
from collections import namedtuple

Node = namedtuple('Node', ['left', 'right'])

def stripReduce(alist, astr):
  astr = astr.strip()
  if astr == '':
    alist += [[]]
  else:
    alist[-1] += [list(astr)]
  return alist

def readlines(file, reduceFn = stripReduce, reduceInit = [[]]):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def isFixable(mismatched):
  mismatched = [(x, y) for x, y in list(zip(mismatched[0], mismatched[1])) if x != y]
  return len(mismatched) == 1

def countMirrorCols(rows, fixSmudges=False):
  mirrored = []
  found = False
  while len(rows) > 0 and not found:
    mirrored = [rows.pop(0)] + mirrored
    mismatched = [(x, y) for x, y in  list(zip(mirrored, rows)) if x != y]
    if len(rows) > 0:
      if not fixSmudges and len(mismatched) == 0:
        found = True
      elif fixSmudges and len(mismatched) == 1 and isFixable(mismatched[0]):
        found = True

  return len(mirrored) if found else 0

def findMirrors(amap, fixSmudges=False):
  rows, cols = list(amap), list(map(list, zip(*amap)))
  return 100 * countMirrorCols(rows, fixSmudges) + countMirrorCols(cols, fixSmudges)
  
maps = readlines(sys.argv[1])
print(sum([findMirrors(amap) for amap in maps]))
print(sum([findMirrors(amap, True) for amap in maps]))


