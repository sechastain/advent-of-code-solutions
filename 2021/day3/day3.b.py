
import sys

ogbytes = [x.strip() for x in open(sys.argv[1], 'r').readlines()]

bytelength = len(ogbytes[0])

print(len(ogbytes))
print(bytelength)
print("--------")

def countOnes(bit, bytes):
  count = 0
  for b in bytes:
    count += (1 if b[bit] == "1" else 0)
  return count

def select(bit, bitval, bytes):
  return [x for x in bytes if x[bit] == bitval]

def o2Criteria(ones, bytes):
  return ones >= len(bytes)/2

def co2Criteria(ones, bytes):
  return ones < len(bytes)/2

def searchFor(bytes, criteria):
  value = 0
  for bit in range(bytelength):
    if len(bytes) == 1:
      return bytes[0]

    ones = countOnes(bit, bytes)

    if criteria(ones, bytes):
      bytes = select(bit, "1", bytes)
    else:
      bytes = select(bit, "0", bytes)

  if len(bytes) == 1:
    return bytes[0]
  else:
    print("NO BUENO " + str(len(bytes)))
    return bytes[0]

def decify(abyte):
  value = 0
  for b in abyte:
    value = value * 2 + (1 if b == "1" else 0)

  return value

o2 = decify(searchFor(ogbytes, o2Criteria))
print(o2)

co2 = decify(searchFor(ogbytes, co2Criteria))
print(co2)

print(o2*co2)
