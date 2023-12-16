
import sys
import re

from functools import reduce

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

def parseLines(lines, line):
  commands = line.strip().split(',')

  return lines + commands

def hash(cmd):
  return reduce(lambda acc, x: (acc + ord(x)) * 17 % 256, list(cmd), 0)

def process(cmd, boxes, labels):
  if '-' in cmd:
    label, _ = cmd.split('-')
    box = hash(label)   
    if label in labels:
      boxes[box] = [l for l in boxes[box] if l[0] != label]
      del labels[label]
  else:
    label, foc = cmd.split('=')
    box = boxes[hash(label)]
    labels[label] = foc
    for l in box:
      if l[0] == label:
        l[1] = foc
        break
    else:
      box.append([label, foc])

def processAll(commands, boxes, labels):
  for cmd in commands:
    process(cmd, boxes, labels)

def scoreBox(id, lenses):
  asum = 0
  for i in range(len(lenses)):
    asum += id * (i+1) * int(lenses[i][1])
  return asum

def scoreBoxes(boxes):
  asum = 0
  for i in range(len(boxes)):
    asum += scoreBox(i+1, boxes[i])
  return asum

commands = readlines(sys.argv[1], parseLines)

print(sum(hash(cmd) for cmd in commands))

boxes = [[] for i in range(256)]
labels = {}
processAll(commands, boxes, labels)
print(scoreBoxes(boxes))

