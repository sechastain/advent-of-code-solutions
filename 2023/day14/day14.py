
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

rotFlip = lambda x: list(map(list, zip(*x[::-1])))

def printMap(amap):
  for row in amap:
    print(''.join(row))

amap = readlines(sys.argv[1])
ops = [rotFlip, rotFlip, rotFlip, rotFlip]

for i in range(1000000000):
  if i %       1000000 == 0:
    print(i)
  amap = reduce(lambda amap, fn: fn(roll(amap)), ops, amap)
print(score(amap))
