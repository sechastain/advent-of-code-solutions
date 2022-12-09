
import re
import sys

from ..utils.io import readlines
from functools import reduce

class Snake:
  def __init__(self, size=2):
    self.knots = list([[0, 0] for i in range(size)])
    self.last = size-1
    self.tracks = set()
    self.tracks.add(tuple(self.knots[self.last]))

  def chase(self, knot):
    lead = self.knots[knot-1]
    tail = self.knots[knot]

    x = abs(lead[0] - tail[0]) == 2
    y = abs(lead[1] - tail[1]) == 2

    if not x and not y:
      return

    ntail = [
      lead[0] if not x else ((lead[0] + tail[0]) // 2),
      lead[1] if not y else ((lead[1] + tail[1]) // 2)
    ]

    self.knots[knot] = ntail
    
    if knot == self.last:
      self.tracks.add(tuple(ntail))
    else:
      self.chase(knot+1)

  def move(self, xy, dir, steps):
    head = self.knots[0]
    while steps > 0:
      head[xy] += dir
      self.chase(1)
      steps -= 1

    return self
        
commands = {
  'U': lambda snake, steps: snake.move(1, 1, steps),
  'D': lambda snake, steps: snake.move(1, -1, steps),
  'L': lambda snake, steps: snake.move(0, -1, steps),
  'R': lambda snake, steps: snake.move(0, 1, steps),
}


def processLine(snake, line):
  [dir, steps] = line[:-1].split(' ')
  return commands[dir](snake, int(steps))

snake = readlines(sys.argv[1], processLine, Snake())
print(len(snake.tracks))

snake = readlines(sys.argv[1], processLine, Snake(10))
print(len(snake.tracks))

