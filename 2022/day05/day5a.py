
import re
import sys

from ..utils.io import readlines
from functools import reduce

stacksInitialized = False
stacks = None

def addBlocks(state, line):
  stacks = state['stacks']

  line = list(line)[1::4]
  if line[0] == '1':
    return

  if stacks is None:
    state['stacks'] = [[s] if s != ' ' else [] for s in line]
  else:
    for i in range(len(line)):
      if line[i] != ' ':
        stacks[i].append(line[i])

def flipBoard(state):
  for s in state['stacks']:
    s.reverse()
  state['stacksInitialized'] = True

def extractInstruction(line):
  return [int(i) for i in re.match('move (\d+) from (\d+) to (\d+)', line).group(1, 2, 3)]

def processInstruction9000(state, line):
  stacks = state['stacks']

  (num, frm, to) = extractInstruction(line)

  while num > 0:
    block = stacks[frm-1].pop()
    stacks[to-1].append(block)
    num -= 1

def processInstruction9001(state, line):
  stacks = state['stacks']

  (num, frm, to) = extractInstruction(line)

  substack = stacks[frm-1][-1*num:]
  stacks[frm-1] = stacks[frm-1][:-1*num]
  stacks[to-1] += substack

def processLine(state, line):
  stacksInitialized = state['stacksInitialized']
  line = line[:-1]

  if not stacksInitialized and line == '':
    flipBoard(state)
  elif not stacksInitialized:
    addBlocks(state, line)
  else:
    state['processFn'](state, line)
  
  state['topline'] = ''.join([l[-1] if len(l) > 0 else ' ' for l in state['stacks']])
  return state

def initState(processFn):
  return {
    'stacksInitialized': False,
    'stacks': None,
    'topline': '',
    'processFn': processFn
  }


print(readlines(sys.argv[1], processLine, initState(processInstruction9000))['topline'])
print(readlines(sys.argv[1], processLine, initState(processInstruction9001))['topline'])


