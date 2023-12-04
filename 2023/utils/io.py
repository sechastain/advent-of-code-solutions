
from functools import reduce

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

