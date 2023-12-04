
import sys

from functools import reduce

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def parseColor(draw):
  draw = draw.strip()
  [count, color] = draw.split(' ')
  return (color, int(count))

def parseColors(draw):
  draw = draw.strip()
  colors = draw.split(',')
  return dict([parseColor(color) for color in colors])

def parseLine(games, line):
  line = line.strip()
  
  [game, draws] = line.split(':')
  game = game.split(' ')[1]
  draws = [parseColors(d) for d in draws.split(';')]

  games[game] = draws
  
  return games

def isPossibleGame(draws, red=12, blue=14, green=13):
  max = {'red': red, 'blue': blue, 'green': green}
  totals = {'red': 0, 'blue': 0, 'green': 0}

  def reduceFn(totals, draw):
    for k in totals.keys():
      totals[k] = draw[k] if k in draw and draw[k] > totals[k] else totals[k]
    return totals

  reduce(reduceFn, draws, totals)

  for k in max.keys():
    if totals[k] > max[k]:
      return False

  return True

def gamePower(draws):
  max = {'red': 0, 'blue': 0, 'green': 0}

  def reduceFn(totals, draw):
    for k in max.keys():
      max[k] = draw[k] if k in draw and draw[k] > max[k] else max[k]
    return totals

  reduce(reduceFn, draws, max)

  return reduce((lambda x, y: x*y), max.values())
  

games = readlines(sys.argv[1], parseLine, {})

possibleScore = [int(g) for g, draws in games.items() if isPossibleGame(draws)]

print(sum(possibleScore))
print(sum([gamePower(draws) for g, draws in games.items()]))

