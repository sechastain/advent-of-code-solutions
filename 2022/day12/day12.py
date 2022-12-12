
import re
import sys

from ..utils.io import readlines
from functools import reduce

def inBounds(point, board):
  return not (point[0] < 0 or point[1] < 0 or point[0] >= len(board) or point[1] >= len(board[0]))

def isValidStepForward(pointa, pointb, board):
  if not inBounds(pointb, board):
    return False

  return board[pointb[0]][pointb[1]] - board[pointa[0]][pointa[1]] <= 1

def isValidStepBackward(pointa, pointb, board):
  if not inBounds(pointb, board):
    return False
  return isValidStepForward(pointb, pointa, board)

def nextPoints(point, board, stepValidator):
  (row, col) = point
  left = (row, col-1)
  right = (row, col+1)
  up = (row-1, col)
  down = (row+1, col)

  ret = [left, right, up, down]
  ret = [r for r in ret if stepValidator(point, r, board)]
  return ret

class Board:
  def __init__(self, board, start, end, stepValidator=isValidStepForward, reverse=False):
    if reverse:
      tmp = start
      start = end
      end = tmp

    self.board = board
    self.start = start
    self.end = end
    self.stepValidator = stepValidator

    self.current = set()
    self.visited = set()
    self.steps = 0

    self.current.add(start)
    self.visited.add(start)

  def nextStep(self):
    self.visited.update(self.current)
    self.steps += 1

    cpoints = self.current
    self.current = set()

    for p in cpoints:
      pnext = nextPoints(p, self.board, self.stepValidator)
      pnext = [pn for pn in pnext if pn not in self.visited]
      self.current.update(pnext)

def isStartToFinishDone(board):
  return board.end in board.current

def isOptimalStartDone(board):
  return 0 in [board.board[p[0]][p[1]] for p in board.current]
    
def findValue(val, board):
  for row in range(len(board)):
    col = board[row].index(val) if val in board[row] else -1
    if col >= 0:
      return (row, col)

def parseBoard(lines, reverse=False):
  a = ord('a')
  z = ord('z')
  S = ord('S') - a
  E = ord('E') - a

  board = [[ord(c) - a for c in list(l)] for l in lines]

  start = findValue(S, board)
  board[start[0]][start[1]] = 0 

  end = findValue(E, board)
  board[end[0]][end[1]] = (z - a)

  stepValidator = isValidStepForward if not reverse else isValidStepBackward

  return Board(board, start, end, stepValidator, reverse)

lines = readlines(sys.argv[1])

board = parseBoard(lines)
while not isStartToFinishDone(board):
  board.nextStep()
print(board.steps)

board = parseBoard(lines, True)
while not isOptimalStartDone(board):
  board.nextStep()
print(board.steps)

