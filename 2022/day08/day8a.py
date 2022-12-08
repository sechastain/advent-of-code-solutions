
import re
import sys

from ..utils.io import readlines
from functools import reduce

board = readlines(sys.argv[1])
board = [list([int(height) for height in list(b)]) for b in board]

def extractRow(board, rowIndex):
  return board[rowIndex]

def extractCol(board, colIndex):
  return list([b[colIndex] for b in board])

# part 1

def findVisibleIndexes(alist):
  alen = len(alist)

  rlist = list(alist)
  rlist.reverse()

  slist = list(alist)
  slist.sort()

  height = slist.pop()
  visible = [alist.index(height)]

  while len(slist) > 0:
    height = slist.pop()
    idx = alist.index(height)
    if idx not in visible and idx < visible[0]:
      visible = [idx] + visible
    else:
      idx = alen - rlist.index(height) - 1
      if idx not in visible and idx > visible[-1]:
        visible.append(idx)

  return visible

def initVizMap(board):
  return [[False for c in b] for b in board]

def processRowViz(board, vizMap):
  for rowIndex in range(len(board)):
    row = extractRow(board, rowIndex)
    for vidx in findVisibleIndexes(row):
      vizMap[rowIndex][vidx] = True

def processColViz(board, vizMap):
  for colIndex in range(len(board[0])):
    col = extractCol(board, colIndex)
    for vidx in findVisibleIndexes(col):
      vizMap[vidx][colIndex] = True


vizMap = initVizMap(board)
processRowViz(board, vizMap)
processColViz(board, vizMap)

print(sum([sum([1 if c else 0 for c in r]) for r in vizMap]))

# part 2

def processDirectedSight(alist, idx, dir):
  alen = len(alist) - 1

  height = alist[idx]

  off = idx + dir

  while off > 0 and off < alen and alist[off] < height:
    off += dir

  return off - idx

def processSight(alist):
  alen = len(alist)
  sight = [0]
  for idx in range(1, alen-1):
    sight.append(
      processDirectedSight(alist, idx, 1) * \
      processDirectedSight(alist, idx, -1) * \
      -1
    )

  sight.append(0)
  
  return sight

def processRowSight(board):
  return [processSight(extractRow(board, idx)) for idx in range(len(board))]

def processColSight(board):
  cols = [processSight(extractCol(board, idx)) for idx in range(len(board[0]))]
  return [[cols[r][c] for r in range(len(cols[c]))] for c in range(len(cols))]

rowSight = processRowSight(board)
colSight = processColSight(board)
mulSight = [[rowSight[r][c] * colSight[r][c] for c in range(len(board[0]))] for r in range(len(board))]
print(max([max(b) for b in mulSight]))

