
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

def up(row, col, amap):
  if row == 0:
    return None
  return (row-1, col)

def down(row, col, amap):
  if row == len(amap)-1:
    return None
  return (row+1, col)

def left(row, col, amap):
  if col == 0:
    return None
  return (row, col-1)

def right(row, col, amap):
  if col == len(amap[row])-1:
    return None
  return (row, col+1)

def mapdir(dir1, dir2):
  def _mapdir(row, col, amap):
    node1 = dir1(row, col, amap)
    node2 = dir2(row, col, amap)
    return None if node1 is None or node2 is None else (node1, node2)
  return _mapdir

pipemap = {
  '|': mapdir(up, down),
  '-': mapdir(left, right),
  'L': mapdir(up, right),
  'J': mapdir(up, left),
  '7': mapdir(left, down),
  'F': mapdir(right, down),
  '.': lambda x, y, z: None,
  'S': lambda x, y, z: 'S',
}

def mapPipes(amap):
  row = 0
  while row < len(amap):
    arow = amap[row]
    col = 0
    while col < len(arow):
      #print(row, col, amap[row][col], arow)
      amap[row][col] = pipemap[amap[row][col]](row, col, amap)
      col += 1
    row += 1

def findStart(amap):
  row = 0
  while row < len(amap):
    if 'S' in amap[row]:
      return (row, amap[row].index('S'))
    row += 1
  print('problem')
  return None

def walkNext(amap, current, prior):
  row, col = current
  options = amap[row][col]
  if options is None:
    return (None, None)
  opt1, opt2 = options
  next = opt1 if opt2 == prior else opt2
  return (next, current)

def findLoop(amap, start):
  row, col = start
  starts = [
    ['up', [row-1, col]],
    ['right', [row+1, col]],
    ['left', [row, col-1]],
    ['right', [row, col+1]],
  ]
  for dir, astart in starts:
    walking = True
    steplog = [start, astart]
    next = astart
    prior = start
    while walking:
      next, prior = walkNext(amap, next, prior)
      if next == None:
        walking = False
      elif next == start:
        return (dir, astart, start, prior, len(steplog), steplog)
      else:
        steplog += [next]
  print('problem - no solution')

def findTwos(amap, zero):
  row, col = zero
  if amap[row][col] == 1:
    return []
  twos = [
#    (row-1, col-1),
    (row-1, col),
#    (row-1, col+1),
    (row, col-1),
    (row, col+1),
#    (row+1, col-1),
    (row+1, col),
#    (row+1, col+1),
  ]
  twos = [(row, col) for row, col in twos if row >=0 and row < len(amap) and col >= 0 and col < len(amap[row])]
  twos = [(row, col) for row, col in twos if amap[row][col] == 2]
  for t in twos:
    row, col = t
    amap[row][col] = 0
  return twos

def doubleLoop(loop):
  dbl = lambda x: int(2*x)
  steps = []
  for s in range(1, len(loop)):
    p = s-1
    prior = loop[p]
    step = loop[s]
    r1, c1 = prior
    r2, c2 = step

    r1 = dbl(r1)
    c1 = dbl(c1)
    r2 = dbl(r2)
    c2 = dbl(c2)

    mid = (int((r1 + r2)/2), int((c1 + c2)/2))
    steps += [(r1, c1), mid]
  r1, c1 = loop[-1]
  r2, c2 = loop[0]
  r1 = dbl(r1)
  c1 = dbl(c1)
  r2 = dbl(r2)
  c2 = dbl(c2)
  steps += [(r1, c1), (int((r1 + r2)/2), int((c1 + c2)/2))]
  #print(steps)
  return steps

def remap(amap, loop):
  loop = doubleLoop(loop)

  amap = [[2] * len(amap[0]) * 2 for m in range(len(amap)*2)]
  amap[0] = [0] * len(amap[0])
  amap[-1] = [0] * len(amap[0])

  for row in amap:
    row[0] = 0
    row[-1] = 0
    #print(''.join(str(s) for s in row))

  for row, col in loop:
    #print(row, col)
    amap[row][col] = 1
  zeroes  = list([(0, i) for i in range(len(amap[ 0]))])
  zeroes += list([(len(amap)-1, i) for i in range(len(amap[-1]))])
  zeroes += list([(i, 0) for i in range(len(amap))])
  zeroes += list([(i, len(amap[i])-1) for i in range(len(amap))])
  #print(zeroes)
  while len(zeroes) > 0:
    zero = zeroes.pop(0)
    zeroes += findTwos(amap, zero)

  for row in amap:
    print(''.join(str(c) for c in row))

  amap = amap[::2]
  amap = [m[::2] for m in amap]
  
  print(sum([row.count(2) for row in amap]))

amap = readlines(sys.argv[1])
mapPipes(amap)
results = findLoop(amap, findStart(amap))
print(results[4]/2)
loopmap = results[5]
remap(amap, loopmap)

