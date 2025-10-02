rng = range(1, 101)
for i in rng:
    if i % 3 == 0:
        if i+3 not in rng:
            # This is the last number divisible by 3 in the range
            print(i)
            # No need to continue the loop
            break
        else:
            print(i, end=', ')