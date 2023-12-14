
import sys
import re

from functools import reduce
from collections import namedtuple

Node = namedtuple('Node', ['left', 'right'])

def stripReduce(alist, astr):
  astr = list(astr.strip())
  return alist + [astr]

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def rollInPlace(amap, row, dir):
  if row == True:
    indexes = list(range(len(amap[0])))[::dir]
    for row in amap:
      next = indexes[0]
      for i in indexes:
        item = row[i]
        if item == '#':
          next = i + dir
        elif item == 'O':
          row[i] = '.'
          row[next] = 'O'
          next = next + dir
  else:
    indexes = list(range(len(amap)))[::dir]
    for c in range(len(amap[0])):
      next = indexes[0]
      for i in indexes:
        item = amap[i][c]
        if item == '#':
          next = i + dir
        elif item == 'O':
          amap[i][c] = '.'
          amap[next][c] = 'O'
          next = next + dir
  return amap

north = lambda amap: rollInPlace(amap, False,  1)
south = lambda amap: rollInPlace(amap, False, -1)
east  = lambda amap: rollInPlace(amap, True,  -1)
west  = lambda amap: rollInPlace(amap, True,   1)

def rollUp(row):
  row = row[:]
  next = 0
  for i in range(len(row)):
    item = row[i]
    if item == '#':
      next = i+1
    elif item == 'O':
      row[i] = '.'
      row[next] = 'O'
      next = next + 1
  return row

def scoreRow(row):
  scores = list(range(1, len(row)+1))[::-1]
  return sum([y for x, y in list(zip(row, scores)) if x == 'O'])

def roll(amap):
  amap = list(map(list, zip(*amap)))
  amap = [rollUp(row) for row in amap]
  amap = list(map(list, zip(*amap)))
  return amap

def score(amap):
  amap = list(map(list, zip(*amap)))
  return sum([scoreRow(row) for row in amap])

def rollAndScore(amap):
  return score(roll(amap))
  
amap = readlines(sys.argv[1])
print(rollAndScore(amap))

def printMap(amap):
  for row in amap:
    print(''.join(row))

encoded = {}
def encode(amap, i):
  key = ''.join([item for row in amap for item in row])
  if key in encoded:
    return True, key
  encoded[key] = i
  return False, key

amap = readlines(sys.argv[1])
for i in range(1000000000):
  east(south(west(north(amap))))
  looped, key = encode(amap, i)
  if looped:
    loops = i - encoded[key]
    loops = (1000000000 - encoded[key] - 1) % loops
    for j in range(loops):
      east(south(west(north(amap))))
    break
print(score(amap))

