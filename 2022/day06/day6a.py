
import re
import sys

from ..utils.io import readlines
from functools import reduce

def buffFinderFn(buffSize):
  def processLine(_, line):
    for off in range(len(line)-buffSize):
      if len(set(line[off:off+buffSize])) == buffSize:
        return off + buffSize
    return -1
  return processLine

print(readlines(sys.argv[1], buffFinderFn(4), ''))
print(readlines(sys.argv[1], buffFinderFn(14), ''))


