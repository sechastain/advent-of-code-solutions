
import sys

from ..utils.io import readlines
from functools import reduce

CAP_ORD_DIFF = -65 + 27
LOWER_ORD_DIFF = -96 + 0

def scoreChar(achar):
  return ord(achar) + (LOWER_ORD_DIFF if ord(achar) >= 97 else CAP_ORD_DIFF)

def scoreLine(total, line):
  line = list(line.strip())

  common = set(line[:len(line)//2]) & set(line[len(line)//2:])

  return total + reduce(lambda x, y: x+scoreChar(y), common, 0)

squad = []
def scoreCommon(total, line):
  line = list(line.strip())

  global squad
  squad = squad + [set(list(line))]
  if len(squad) == 3:
    squadScore = scoreChar(next(iter(reduce(lambda x, y: x & y, squad))))
    squad = []
    return total + squadScore
  else:
    return total

print(readlines(sys.argv[1], scoreLine, 0))

print(readlines(sys.argv[1], scoreCommon, 0))


