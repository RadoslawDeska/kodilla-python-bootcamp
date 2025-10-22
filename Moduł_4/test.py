a = 1

def demo():
    a = 2
    print(a)

demo()
print(a)
print(type(None))

def fun_default(p1, p2=2, p3=3):
    pass
def fun_positional(p1, p2, p3, /):
    pass
def fun_keyword(*, p1, p2, p3):
    pass

funs = [fun_default, fun_positional, fun_keyword]

for fun in funs:
    print(fun.__name__)
    try:
        print("Wszystkie pozycyjne", end=": ")
        fun(1, 2, 3)
    except TypeError as e:
        print(e)
    else:
        print("OK")
    try:
        print("Dwa pozycyjne i jeden nazwany", end=": ")
        fun(1, 2, p3=3)
    except TypeError as e:
        print(e)
    else:
        print("OK")
    try:
        print("Jeden pozycyjny i dwa nazwane", end=": ")
        fun(1, p2=2, p3=3)
    except TypeError as e:
        print(e)
    else:
        print("OK")
    try:
        print("Wszystkie nazwane", end=": ")
        fun(p1=1, p2=2, p3=3)
    except TypeError as e:
        print(e)
    else:
        print("OK")
    
    print()


def count_them_all(*args, **kwargs):
    positional_args_count = len(args)
    kword_args_count = len(kwargs)
    print(f"I have received {positional_args_count} positional arguments")
    print(f"and {kword_args_count} keyword arguments.")

count_them_all(1, 2, 3, "A")
count_them_all(1, 2, 3 , "A", new=True)