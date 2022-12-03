
import sys

from ..utils.io import readlines

calories = readlines(sys.argv[1])

elf = 0

elves = {}

for cal in calories:
  if cal == '':
    elf += 1
  else:
    elves[elf] = elves.get(elf, 0) + int(cal)

elf_cals = list(elves.values())

elf_cals.sort()

print(elf_cals[-1])
print(sum(elf_cals[-3:]))



