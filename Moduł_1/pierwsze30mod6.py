i = 1
divisible = []
while True:
    if i % 6 == 0:
        divisible.append(i)
        if len(divisible) == 30:
            for j, num in enumerate(divisible):
                if j == len(divisible) - 1:
                    print(num)
                else:
                    print(num, end=', ')
            break
    i += 1