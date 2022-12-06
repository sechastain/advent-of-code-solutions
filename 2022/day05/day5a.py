
import re
import sys

from ..utils.io import readlines
from functools import reduce

stacksInitialized = False
stacks = None

def addBlocks(line):
  global stacks, stacksInitialized

  line = list(line)[1::4]
  if line[0] == '1':
    return

  if stacks is None:
    stacks = [[s] if s != ' ' else [] for s in line]
  else:
    for i in range(len(line)):
      if line[i] != ' ':
        stacks[i].append(line[i])

def flipBoard():
  global stacks, stacksInitialized

  for s in stacks:
    s.reverse()
  stacksInitialized = True

def extractInstruction(line):
  return [int(i) for i in re.match('move (\d+) from (\d+) to (\d+)', line).group(1, 2, 3)]

def processInstruction9000(line):
  global stacks, stacksInitialized

  (num, frm, to) = extractInstruction(line)

  while num > 0:
    block = stacks[frm-1].pop()
    stacks[to-1].append(block)
    num -= 1

def processLine9000(_, line):
  global stacks, stacksInitialized

  line = line[:-1]

  if not stacksInitialized and line == '':
    flipBoard()
  elif not stacksInitialized:
    addBlocks(line)
  else:
    processInstruction9000(line)
  
  return ''.join([l[-1] if len(l) > 0 else ' ' for l in stacks])

def processInstruction9001(line):
  global stacks, stacksInitialized

  (num, frm, to) = extractInstruction(line)

  substack = stacks[frm-1][-1*num:]
  stacks[frm-1] = stacks[frm-1][:-1*num]
  stacks[to-1] += substack

def processLine9001(_, line):
  global stacks, stacksInitialized

  line = line[:-1]

  if not stacksInitialized and line == '':
    flipBoard()
  elif not stacksInitialized:
    addBlocks(line)
  else:
    processInstruction9001(line)
  
  return ''.join([l[-1] if len(l) > 0 else ' ' for l in stacks])


print(readlines(sys.argv[1], processLine9000, 0))

stacksInitialized = False
stacks = None

print(readlines(sys.argv[1], processLine9001, 0))

