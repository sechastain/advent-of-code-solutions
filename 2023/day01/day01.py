
import sys

from functools import reduce

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def parseLine(sum, line):
  line = list(line)
  line = [l for l in line if l >= '0' and l <= '9']
  num = (int(line[0]) * 10 + int(line[-1])) if len(line) > 0 else 0

  return sum + num

values = {
  '1': 1,
  'one': 1,
  '2': 2,
  'two': 2,
  '3': 3,
  'three': 3,
  '4': 4,
  'four': 4,
  '5': 5,
  'five': 5,
  '6': 6,
  'six': 6,
  '7': 7,
  'seven': 7,
  '8': 8,
  'eight': 8,
  '9': 9,
  'nine': 9,
  '0': 0,
  'zero': 0,
}
def parseLine2(sum, line):
  leftIndex = None
  left = None
  rightIndex = None
  right = None
  for v in values.keys():
    value = values[v]
    off = 0
    try:
      while True:
        off = line.index(v, off)
        if leftIndex is None or leftIndex > off:
          leftIndex = off
          left = value
        if rightIndex is None or rightIndex < off:
          rightIndex = off
          right = value
        off += 1
    except:
      pass

  return sum + left * 10 + right
  

sum = readlines(sys.argv[1], parseLine, 0)
print(sum)
sum = readlines(sys.argv[1], parseLine2, 0)
print(sum)

