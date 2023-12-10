
import sys
import re

from functools import reduce
from collections import namedtuple

Node = namedtuple('Node', ['left', 'right'])

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def parseLine(nums, line):
  lnums = [int(n) for n in line.strip().split(' ')]
  return nums + [lnums]

def findNext(nums, sign=1):
  if nums.count(0) == len(nums):
    return nums + [0]
  else:
    smaller = findNext([x-y for x, y in list(zip(nums[1:], nums[:-1]))], sign)

    if sign == 1:
      return nums + [nums[-1] +  smaller[-1]]
    else:
      return [nums[0] - smaller[0]] + nums


nums = readlines(sys.argv[1], parseLine, [])
print(sum([findNext(lnum)[-1] for lnum in nums]))
nums = readlines(sys.argv[1], parseLine, [])
print(sum([findNext(lnum, -1)[0] for lnum in nums]))

