
import re
import sys

from ..utils.io import readlines
from functools import reduce

def buffFinderFn(buffSize):
  def processLine(_, line):
    off = 0

    found = False
    while not found:
      if len(set(line[off:off+buffSize])) == buffSize:
        found = True
      else:
        off += 1
    return off + buffSize
  return processLine

print(readlines(sys.argv[1], buffFinderFn(4), ''))
print(readlines(sys.argv[1], buffFinderFn(14), ''))


