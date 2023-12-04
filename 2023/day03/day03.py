
import sys
import re

from functools import reduce

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def parseLine(lines, line):
  line = line.strip()
  numbers = re.findall(r'\d+', line)
  off = 0
  matches = {}
  for n in numbers:
    off = line.index(n, off)
    matches[off] = int(n)
    off += len(n)
  return lines + [(line, matches)]

def getBounds(line, off, num):
  left = off if off == 0 else (off-1)
  right = off + len(str(num)) 
  right = right if right < len(line) else (right-1)
  return (left, right)

def symbolInBounds(text, left, right, regex=r'[^\d\d.]'):
  text = text[left:right+1]
  matches = re.findall(regex, text)
  return matches is not None and len(matches) > 0

def filterSymbolAdjacentNumbers(lines):
  first = lines[0]
  last = lines[-1]
  lindex = 0
  numbers = []

  for line in lines:
    text, matches = line
    for off, num in matches.items():
      left, right = getBounds(text, off, num)

      touched = False
      if line != first:
        touched = touched or symbolInBounds(lines[lindex-1][0], left, right)
      touched = touched or symbolInBounds(lines[lindex][0], left, right)
      if line != last:
        touched = touched or symbolInBounds(lines[lindex+1][0], left, right)

      if touched:
        numbers.append(num)

      off += 1
      
    lindex += 1

  return numbers

def findGearPotentials(lines):
  lindex = 0
  gears = []
  for line in lines:
    off = 0
    text = line[0]
    try:
      while True:
        off = text.index('*', off)
        gears.append((lindex, off))
        off += 1
    except:
      pass
    lindex += 1

  return gears

def findGears(potentials, lines):
  products = []
  for gear in potentials:
    line, col = gear
    up = 0 if line == 0 else (line-1)
    down = (line+1) if line < len(lines)-1 else line
    adjacent = []
    for l in lines[up:down+1]:
      text, matches = l
      for off, num in matches.items():
        left = off if off == 0 else off-1
        right = off + len(str(num))
        right = right if right < len(text) else (right-1)
        if left <= col and col <= right:
          adjacent.append(num)

    if len(adjacent) > 2:
      print('problem', gear, adjacent)
    elif len(adjacent) == 2:
      products.append(reduce((lambda x, y: x*y), adjacent))

  return sum(products)
      

lines = readlines(sys.argv[1], parseLine, [])
numbers = filterSymbolAdjacentNumbers(lines)
print(sum(numbers))

gears = findGearPotentials(lines)
print(findGears(gears, lines))

