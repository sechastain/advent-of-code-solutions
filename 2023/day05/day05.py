
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

def parseHeader(maps, line):
  line = line.split(':')
  if line[-1] == '':
    name, _ = line[0].split(' ')
    name = name.split('-')
    source = name[0]
    destination = name[-1]
    section = {
      'source': source,
      'destination': destination,
      'ranges': []
    }
    maps[source] = section
    maps['current'] = section
  else:
    line = line[1].strip()
    maps['origin'] = [int(n) for n in line.split(' ')]
    

def parseLine(maps, line):
  line = line.strip()
  if line == '':
    pass
  elif ':' in line:
    parseHeader(maps, line)
  else:
    maps['current']['ranges'] += [list([int(n) for n in line.split(' ')])]
  
  return maps

def findDestination(seed, ranges):
  ranges = [r for r in ranges if r[1] <= seed and seed < r[1] + r[2]]
  if len(ranges) == 0:
    return seed
  else:
    r = ranges[0]
    return r[0] - r[1] + seed

def walkSeedsToDestination(seeds, origin, destination, maps):
  while origin != destination:
    amap = maps[origin]
    seeds = [findDestination(seed, amap['ranges']) for seed in seeds]
    origin = amap['destination']

  return seeds

def originToLocation(maps):
  seeds = maps['origin']
  origin = 'seed'
  destination = 'location'
  return walkSeedsToDestination(seeds, origin, destination, maps)

def mapRange(seed, range):
  #print(seed)
  seedMin, seedLen = seed
  seedMax = seedMin + seedLen - 1
  destMin, sourceMin, mapLen = range
  sourceMax = sourceMin + mapLen - 1
  destMax = destMin + mapLen - 1

  if seedMax >= sourceMin and seedMin <= sourceMax:
    if seedMin >= sourceMin and seedMax <= sourceMax:
      return [(destMin - sourceMin + seedMin, seedLen)]
    elif seedMin < sourceMin and seedMax > sourceMax:
      # returning 3 tuples
      return [(destMin, mapLen), (seedMin, sourceMin - seedMin), (sourceMax + 1, seedMin + seedLen - sourceMax - 1)]
    elif seedMin < sourceMin:
      return [(destMin, seedMin + seedLen - sourceMin), (seedMin, sourceMin - seedMin)]
    elif seedMax > sourceMax:
      return [(destMin - sourceMin + seedMin, sourceMin + mapLen - seedMin), (sourceMin + mapLen, seedMin + seedLen - sourceMin - mapLen)]
      #return [(destMax + sourceMax - seedMin, sourceMax - seedMin), (sourceMax + 1, seedLen + sourceMax - seedMin + 1)]
    else:
      print('problem')
  else:
    return [seed]
  

def findDestination2(seed, ranges):
  mapped = []
  unmapped = [seed]
  while len(unmapped) > 0:
    aseed = unmapped.pop(0)
    foundMap = False
    for range in ranges:
      results = mapRange(aseed, range)
      if results[0] != aseed:
        mapped += [results.pop(0)]
        unmapped += results
        foundMap = True
        break
    if not foundMap:
      mapped += [aseed]

  return mapped

def walkSeedsToDestination2(seeds, origin, destination, maps):
  while origin != destination:
    amap = maps[origin]
    print(seeds)
    seeds = [findDestination2(seed, amap['ranges']) for seed in seeds]
    seeds = [seed for seedlist in seeds for seed in seedlist]
    origin = amap['destination']

  return seeds

def originToLocation2(maps):
  seeds = maps['origin']
  seeds = list(zip(seeds[0::2], seeds[1::2]))
  origin = 'seed'
  destination = 'location'
  return walkSeedsToDestination2(seeds, origin, destination, maps)


maps = {
  'current': None
}
readlines(sys.argv[1], parseLine, maps)
print(min(originToLocation(maps)))
print(min([x[0] for x in originToLocation2(maps)]))


