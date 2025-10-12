num = 30
fibonacci = []

for i in range(0,num):
    if i <= 1:
        fibonacci.append(1)
    else:
        fibonacci.append(sum(fibonacci[-2:]))

print(fibonacci)