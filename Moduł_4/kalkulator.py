from functools import wraps
import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

operators = {}

def register(op):
    def decorator(func):
        @wraps(func)
        def wrapper():
            return
        operators[op] = func
        return wrapper
    return decorator


@register("+")
def add(*args):
    """Dodaje argumenty"""
    result = 0
    for arg in args:
        result += arg
    return result

@register("-")
def subtract(*args):
    """Odejmuje argumenty"""
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result

@register("*")
def multiply(*args):
    """Mnoży argumenty"""
    result = 1
    for arg in args:
        result *= arg
    return result

@register("/")
def divide(*args):
    """Dzieli argumenty"""
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result


def get_operation():
    """Pobiera od użytkownika rodzaj działania"""
    op = input(f"Podaj działanie {''.join(operators.keys())}: ")
    return op

def get_number():
    """Pobiera od użytkownika liczbę"""
    inp = float(input("Podaj liczbę: "))
    return inp

def ask_more():
    """Pobiera od użytkownika kolejną liczbę (przy więcej niż dwóch argumentach wybranej operacji)"""
    num = input("Podaj liczbę lub [Enter] by podać wynik: ")
    if num == "":
        return False
    return num  # Uwzględnia zero!

def get_more(numbers: list):
    while True:
        number = ask_more()
        if number:
            numbers.append(float(number))
        else:
            break
    return numbers

def main():
    op = get_operation()
    numbers = []
    
    for _ in range(2):
        number = get_number()
        numbers.append(number)
    
    if op in ["+", "*"]:  # opcja do operacji na więcej niż 2 argumentach
        numbers = get_more(numbers)
    
    result = operators[op](*numbers)
    
    print(f"{op.join([str(num) for num in numbers])} = {result}")


if __name__ == "__main__":
    main()