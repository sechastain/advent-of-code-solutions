
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

def parseLine(maps, line):
  line = line.strip()
  if line == '':
    pass
  elif ':' in line:
    parseHeader(maps, line)
  else:
    maps['current']['ranges'] += [list([int(n) for n in line.split(' ')])]
  
  return maps

def possibleWins(game):
  ms, max = game
  return len([charge * (ms - charge) for charge in range(0, ms+1) if charge * (ms - charge) > max])


sample = [(7, 9), (15, 40), (30, 200)]
input = [(56, 499), (97, 2210), (77, 1097), (93, 1440)]

sampleWins = [possibleWins(game) for game in input]
print(sampleWins)
print(reduce((lambda x, y: x*y), sampleWins))

print(possibleWins((56977793, 499221010971440)))

