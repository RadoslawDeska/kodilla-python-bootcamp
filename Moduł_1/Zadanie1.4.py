def print_nr1():
    print("Nr 1")
    for i in range(10):
        if i % 2 == 0:
            print("* "*10)
        else:
            print(" *"*10)
    print()

def print_nr2():
    print("Nr 2")
    for i in range(1,11):
        if i % 2 == 0:
            print("*"*i)
        else:
            print("*"*(i+1))
    print()

def print_nr3():
    print("Nr 3")
    for i in range(6,0,-1):
        print("*"*i)
    print()

print_nr1()
print_nr2()
print_nr3()