
import re
import sys

from ..utils.io import readlines
from functools import reduce

class Device:
  def __init__(self):
    self.cycles = [1]
    self.crt = [['.'] * 40 for i in range(6)]

  def updateCrt(self):
    pos = self.cycles[-1]
    pixels = [i for i in list(range(pos-1, pos+2)) if i >= 0 and i < 40]

    cycle = len(self.cycles) - 1
    row = cycle // 40
    col = cycle %  40

    if col in pixels:
      self.crt[row][col] = '#'

  def noop(self):
    x = self.cycles[-1]
    self.updateCrt()
    self.cycles.append(x)
    return self

  def addx(self, value):
    x = self.cycles[-1]
    self.updateCrt()
    self.cycles.append(x)
    self.updateCrt()
    self.cycles.append(x + value)
    return self

commands = {
  'noop': lambda state, value: state.noop(),
  'addx': lambda state, value: state.addx(value)
}

def processLine(state, line):
  cmd, *val = line[:-1].split(' ')
  val = int(val[0]) if val != [] else None
  return commands[cmd](state, val)

state = readlines(sys.argv[1], processLine, Device())
print(sum([state.cycles[i-1] * (i) for i in range(20, 221, 40)]))
print('\n'.join([''.join(row) for row in state.crt]))

