
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

def parseLine(cards, line):
  line = line.strip()
  card, nums = line.split(':')
  card = int(card.split(' ')[-1])

  winning, mine = nums.split('|')
  winning = [int(w) for w in winning.strip().split(' ') if w != '']
  mine = [int(m) for m in mine.strip().split(' ') if m != '']

  cards[card] = {
    'winning': winning,
    'mine': mine
  }
  return cards

def countWins(card):
  winning = card['winning']
  mine = card['mine']

  return len([m for m in mine if m in winning])

def scoreCard(card):
  wins = countWins(card)
  return 2**(wins-1) if wins > 0 else 0

def playGame(cards):
  numPlays = {c: 1 for c in cards.keys()}
  id = 1
  
  while id in cards.keys():
    playCount = numPlays[id]
    card = cards[id]
    wins = countWins(card)
    if wins > 0:
      for cid in range(id+1, id+wins+1):
        numPlays[cid] += playCount
    id += 1

  return sum(numPlays.values())

cards = readlines(sys.argv[1], parseLine, {})
print(sum([scoreCard(c) for c in cards.values()]))
print(playGame(cards))

