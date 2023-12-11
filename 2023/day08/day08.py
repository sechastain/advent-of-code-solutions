
import sys
import re

from functools import reduce
from collections import namedtuple
import struct

Node = namedtuple('Node', ['left', 'right', 'exit', 'bitmask'])

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  directions = list(lines[0].strip())
  directions = [0 if d == 'L' else 1 for d in directions]
  reduceInit['dirs'] = directions

  lines = lines[2:]
  return reduce(reduceFn, lines, reduceInit)

def parseLine(nodes, line):
  line = line.strip()
  node, leftright = line.split(' = ')
  left, right = leftright.split(', ')
  left = left[1:]
  right = right[0:-1]

  nodes[node] = Node(left, right, None, None)
  
  return nodes

def walkIt(directions, nodes, start, end=None):
  i = 0
  node = start
  dirs = directions[0:]
  while node != end and node[-1] != 'Z':
    i += 1
    dir = dirs.pop(0)
    node = nodes[node][dir]
    if len(dirs) == 0:
      dirs = directions[0:]
    
  return i, node


def walk(directions, nodes, start='AAA'):
  return walkIt(directions, nodes, 'AAA', 'ZZZ')[0]

def inputMap(directions, nodes):
  for node, ntuple in nodes.items():
    if node == 'dirs':
      continue
    current = node
    bitmask = []
    for dir in directions:
      current = nodes[current][dir]
      bitmask += [1 if current[-1] == 'Z' else 0]
    nodes[node] = Node(ntuple.left, ntuple.right, current, int(''.join(str(b) for b in bitmask), 2))

def ghostwalk(directions, nodes):
  current = [n for n in nodes.keys() if n[-1] == 'A']
  print([(c, walkIt(directions, nodes, c)) for c in current])
  

def ghostwalk2(directions, nodes):
  inputMap(directions, nodes)
  print('done mapping')
  current = [n for n in nodes.keys() if n[-1] == 'A']
  iter = 0
  while True:
    if iter % 100000 == 0:
      print('status', iter)
    #print(current)
    bitmasks = [nodes[n].bitmask for n in current]
    #print(bitmasks)
    bitmasks = reduce(lambda x, y: x & y, bitmasks)
    if bitmasks != 0:
      print('found', iter, len(directions), bitmasks)
      bitmasks = "{0:b}".format(bitmasks)
      print(bitmasks)
      return iter * len(directions) + bitmasks.index('1') + 1
    current = [nodes[n].exit for n in current]
    iter += 1

    

def ghostwalkLongtime(directions, nodes):
  i = 0
  node = [n for n in nodes.keys() if n[-1] == 'A']
  print('start', node)
  dirs = directions[0:]
  while True:
    i += 1
    dir = dirs.pop(0)
    print('before', node)
    node = [nodes[n][dir] for n in node]
    print('after ', node)
    zcount = reduce(lambda x, y: x + (1 if y[-1] == 'Z' else 0), node, 0)
    if len(node) == zcount:
      return i
    if len(dirs) == 0:
      dirs = directions[0:]

nodes = readlines(sys.argv[1], parseLine, {})
#print(nodes)
print(walk(nodes['dirs'], nodes))
print(ghostwalk(nodes['dirs'], nodes))

