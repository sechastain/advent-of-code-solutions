
import sys

depths = [int(x) for x in open(sys.argv[1], 'r').readlines()]

greater = 0
for i in range(1, len(depths)):
  if depths[i] > depths[i-1]:
    greater += 1

print("Greater " + str(greater))
