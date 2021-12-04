
import sys

depths = [int(x) for x in open(sys.argv[1], 'r').readlines()]

slide = []
for i in range(2, len(depths)):
  slide.append(depths[i-2] + depths[i-1] + depths[i])

greater = 0
for i in range(1, len(slide)):
  if slide[i] > slide[i-1]:
    greater += 1

print("Greater " + str(greater))

