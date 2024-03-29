
import sys

from ..utils.io import readlines
from functools import reduce

def make_range(input):
  input = [int(i) for i in input.split('-')]
  input[-1] += 1
  return set(range(*input))

def scoreLine(total, line):
  [first, second] = [make_range(l) for l in line.strip().split(',')]
  overlap = first & second
  return total + (1 if overlap in [first, second] else 0)

def scoreAnyOverlap(total, line):
  [first, second] = [make_range(l) for l in line.strip().split(',')]
  overlap = first & second
  return total + (1 if len(overlap) > 0 else 0)

print(readlines(sys.argv[1], scoreLine, 0))

print(readlines(sys.argv[1], scoreAnyOverlap, 0))

