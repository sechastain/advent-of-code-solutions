
import re
import sys
import json

from ..utils.io import readlines
from functools import reduce, cmp_to_key

def isValidIntPair(left, right):
  if left < right:
    return 'valid'
  elif left == right:
    return 'continue'
  else:
    return 'invalid'
    
def isValidListPair(left, right):
  llen = len(left)
  rlen = len(right)
  validity = None
  for i in range(llen):
    if i == rlen and i < llen:
      return 'invalid'
    validity = isValidPair((left[i], right[i]))
    if validity != 'continue':
      return validity
  if llen == rlen:
    return "continue"
  return 'valid'

validChecks = {
  "('int', 'int')": isValidIntPair,
  "('list', 'list')": isValidListPair,
  "('list', 'int')": lambda x, y: isValidListPair(x, [y]),
  "('int', 'list')": lambda x, y: isValidListPair([x], y),
}

def isValidPair(pair):
  tpair = str(tuple([type(p).__name__ for p in pair]))
  return validChecks[tpair](*pair)

def isValidCompare(left, right):
  ret = -1 if isValidPair((left, right)) != 'invalid' else 1
  return ret

def parsePair(pair):
  return (json.loads(pair[0]), json.loads(pair[1]))

def parseLines(lines):
  return [parsePair(lines[i:i+3]) for i in range(0, len(lines), 3)]

pairs = parseLines(readlines(sys.argv[1]))

print(sum([i+1 for i in range(len(pairs)) if isValidPair(pairs[i]) != 'invalid']))

pairs = [p for pair in pairs for p in pair]
pairs.extend([[[2]], [[6]]])
pairs.sort(key=cmp_to_key(isValidCompare))
print(reduce(lambda x, y: x*y, [i+1 if pairs[i] in [[[2]], [[6]]] else 1 for i in range(len(pairs))], 1))

