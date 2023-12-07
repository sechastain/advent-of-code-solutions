
import sys
import re

from functools import reduce
from collections import namedtuple

def stripReduce(alist, astr):
  return alist + [astr.strip()] 

def readlines(file, reduceFn = stripReduce, reduceInit = []):
  lines = []
  
  with open(file, 'r') as f:
    lines = f.readlines()

  return reduce(reduceFn, lines, reduceInit)

cardValues = {
  '2': 2,
  '3': 3,
  '4': 4,
  '5': 5,
  '6': 6,
  '7': 7,
  '8': 8,
  '9': 9,
  'T': 10,
  'J': 11,
  'Q': 12,
  'K': 13,
  'A': 14,
}

cardValues2 = cardValues
cardValues2['J'] = 0

types = [
  (5,),
  (4, 1),
  (3, 2),
  (3, 1, 1),
  (2, 2, 1),
  (2, 1, 1, 1,),
  (1, 1, 1, 1, 1,)
]

Hand = namedtuple('Hand', ['cards', 'values', 'type', 'typeScore', 'bid'])

def parseLine(hands, line):
  line = line.strip()
  cards, bid = line.split(' ')

  bid = int(bid)

  cards = list(cards)

  values = [cardValues[c] for c in cards]

  handtype = {}
  for v in values:
    handtype[v] = (handtype[v] + 1) if v in handtype else 1
  handtype = list(handtype.values())
  handtype.sort(reverse=True)
  handtype = tuple(handtype)

  hand = [Hand(cards, values, handtype, types.index(handtype), bid)]
  
  return hands + hand

def parseLine2(hands, line):
  line = line.strip()
  cards, bid = line.split(' ')

  bid = int(bid)

  cards = list(cards)

  values = [cardValues[c] for c in cards]

  handtype = {}
  for v in values:
    handtype[v] = (handtype[v] + 1) if v in handtype else 1
  jokers = 0
  if 0 in handtype:
    jokers = handtype[0]
    del handtype[0]
  handtype = list(handtype.values())
  handtype.sort(reverse=True)
  if len(handtype) > 0:
    handtype[0] += jokers
  else:
    handtype = (5,)
  handtype = tuple(handtype) 

  hand = [Hand(cards, values, handtype, types.index(handtype), bid)]
  
  return hands + hand


def scoreHands(parser):
  hands = readlines(sys.argv[1], parser, [])
  hands.sort(key=lambda hand: hand.values)
  hands.sort(key=lambda hand: hand.typeScore, reverse=True)
  rank = range(1, len(hands)+1)
  hands = zip(hands, rank)
  print(reduce(lambda acc, res: acc + res[0].bid * res[1], hands, 0))

scoreHands(parseLine)
scoreHands(parseLine2)
