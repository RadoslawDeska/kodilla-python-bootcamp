cubes = [i ** 3 for i in range(1,11)]
for i in cubes:
  if i % 2 != 0:
    print(i, end=" ")
print()

listing = [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 3, 0, 0]
zeros = listing[1:4] + listing[5:-4] + listing[-2:]
positive = listing[0:1] + listing[4:5] + listing[-4:-2]
print(zeros)
print(positive)
