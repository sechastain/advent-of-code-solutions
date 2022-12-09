
import re
import sys

from ..utils.io import readlines
from functools import reduce

class Snake:
  def __init__(self):
    self.head = [0, 0]
    self.tail = [0, 0]
    self.tracks = set()
    self.tracks.add(tuple(self.tail))

  def move(self, xy, dir, steps):
    while steps > 0:
      self.head[xy] += dir
      if abs(self.head[xy] - self.tail[xy]) > 1:
        self.tail = list(self.head)
        self.tail[xy] -= dir
        self.tracks.add(tuple(self.tail))
      steps -= 1

    return self
        
commands = {
  'U': lambda snake, steps: snake.move(1, 1, steps),
  'D': lambda snake, steps: snake.move(1, -1, steps),
  'L': lambda snake, steps: snake.move(0, 1, steps),
  'R': lambda snake, steps: snake.move(0, -1, steps),
}



def processLine(snake, line):
  [dir, steps] = line[:-1].split(' ')
  return commands[dir](snake, int(steps))

snake = readlines(sys.argv[1], processLine, Snake())
print(len(snake.tracks))

