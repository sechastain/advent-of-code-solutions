
import sys

from ..utils.io import readlines

theirs = {
  'A': 1,
  'B': 2,
  'C': 3,
}

ours = {
  'X': 1,
  'Y': 2,
  'Z': 3,
}

wins = {
  'X': 'C',
  'Y': 'A',
  'Z': 'B',
}

directed = {
  'X': {
    'A': 'C',
    'B': 'A',
    'C': 'B',
  },
  'Y': {
    'A': 'A',
    'B': 'B',
    'C': 'C',
  },
  'Z': {
    'A': 'B',
    'B': 'C',
    'C': 'A',
  }
}

def scoreLine(total, line):
  line = line.strip()
  if line == '':
    return total

  [them, us] = line.split(' ')
  total += ours[us]
  total += 3 if theirs[them] == ours[us] else 6 if wins[us] == them else 0

  return total

def scoreFudgedLine(total, line):
  line = line.strip()
  if line == '':
    return total

  [them, dir] = line.split(' ')

  us = directed[dir][them]

  return total + theirs[us] + (3 if dir == 'Y' else 6 if dir == 'Z' else 0)

print(readlines(sys.argv[1], scoreLine, 0))

print(readlines(sys.argv[1], scoreFudgedLine, 0))

