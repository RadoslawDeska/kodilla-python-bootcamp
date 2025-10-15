def is_divisible(num, div):
    if all(isinstance(arg, int) for arg in (num, div)):
        if div == 0:
            raise ValueError("The divisor cannot be zero.")
        else:
            return num % div == 0
    raise ValueError("Both arguments must be integer numbers.")

if __name__ == "__main__":
    try:
        assert is_divisible(10, 0)
    except ValueError as e:
        pass
    try:
        assert is_divisible(10, 2.5)
    except ValueError as e:
        pass
    assert is_divisible(10, 2) == True
    assert is_divisible(10, 3) == False

    divisible = [i for i in range(101) if is_divisible(i, 5)]
    print(divisible)
    print([i **3 for i in divisible])
