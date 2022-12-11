
import re
import sys

from ..utils.io import readlines
from functools import reduce

operators = {
  '*': lambda x, y : x * y,
  '+': lambda x, y : x + y,
}

class Test:
  def __init__(self, testDiv, tmonkey, fmonkey):
    self.testDiv = testDiv
    self.tmonkey = tmonkey
    self.fmonkey = fmonkey

  def test(self, testValue, monkeys):
    amonkey = self.tmonkey if testValue % self.testDiv == 0 else self.fmonkey
    monkeys[amonkey].add_item(testValue)
    

class Monkey:
  def __init__(self, id, items, op, test):
    self.id = id
    self.items = items
    self.op = op
    self.test = test
    self.inspections = 0

  def add_item(self, item):
    self.items.append(item)

  def _op(self, item):
    [left, op, right] = self.op
    left = item if left == 'old' else int(left)
    right = item if right == 'old' else int(right)
    return operators[op](left, right)

  def inspect(self, monkeys, worryFn):
    while len(self.items) > 0:
      self.inspections += 1
      item = self.items.pop(0)
      item = self._op(item)
      item = worryFn(item)
      self.test.test(item, monkeys)

def play(monkeys, rounds, worryFn):
  while rounds > 0:
    [m.inspect(monkeys, worryFn) for m in monkeys]
    rounds -= 1

  inspections = list([m.inspections for m in monkeys])
  inspections.sort()
  print(inspections[-1] * inspections[-2])

def defaultWorry(value):
  return value // 3

def managedWorry(monkeys):
  testDivs = [m.test.testDiv for m in monkeys]
  worry = reduce(lambda x, y: x * y, testDivs, 1)
  def worryFn(value):
    return value % worry
  return worryFn

def parseMonkey(mtext):
  mid = int(mtext[0].split(' ')[1].split(':')[0])
  mitems = [int(i.strip()) for i in mtext[1].split(':')[1].strip().split(',')]
  mop = mtext[2].split('=')[1].strip().split(' ')
  mtest = int(mtext[3].split(' ')[-1])
  mtrue = int(mtext[4].split(' ')[-1])
  mfalse = int(mtext[5].split(' ')[-1])

  return Monkey(mid, mitems, mop, Test(mtest, mtrue, mfalse))

def parseLines(lines):
  mtext = [lines[i:i+7] for i in range(0, len(lines), 7)]
  return [parseMonkey(mt) for mt in mtext]

lines = readlines(sys.argv[1])

monkeys = parseLines(lines)
play(monkeys, 20, defaultWorry)

monkeys = parseLines(lines)
play(monkeys, 10000, managedWorry(monkeys))

