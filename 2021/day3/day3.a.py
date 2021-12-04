
import sys

bytes = [x.strip() for x in open(sys.argv[1], 'r').readlines()]

positions = {}

for b in bytes:
  for i in range(len(b)):
    positions[i] = positions.get(i, 0) + (1 if b[i] == "1" else 0)

gamma = 0
epsilon = 0

print(len(bytes))
print(len(positions))
print(positions.keys())

for i in range(len(positions)):
  gbit = 1 if positions[i] > len(bytes)/2 else 0
  ebit = 1 if gbit == 0 else 0
  gamma = (gamma * 2) + gbit
  epsilon = (epsilon * 2) + ebit

print(gamma)
print(epsilon)
print(gamma * epsilon)

