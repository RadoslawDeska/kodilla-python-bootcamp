# Zadanie 1
name_list = ["John", "Michael", "Terry", "Eric", "Graham"]
name_dictionary = {name: len(name) for name in name_list}

# Zadanie 2
def is_prime(n):
    """Check if a number is prime."""
    if not isinstance(n, int):
        raise TypeError("Provide integer larger than 1.")
    if n < 2:
        raise ValueError("A prime is a natural number greater than 1.")
    if n == 2:
        return True  # 2 is prime
    for i in range(2, int(n**0.5) + 1):  # Check at most sqrt(n)
        if n % i == 0:  # Return at the first hit of additional divisor
            return False
    return True
nums = [1, 2, 3, 5, 6, 11, 12, 18, 19, 21]

# Zadanie 3
wk_days = ['pon','śro','pią','sob']

# Zadanie 3a
"""Dni tygodnia z poprzedniej wersji zadania, posortowane według kolejności w kalendarzu."""
wk_days_dict = {'pon': 0, 'wt': 1, 'śro': 2, 'czw': 3, 'pią': 4, 'sob': 5, 'nie': 6}

# Zadanie 4
instructions = ["włącz czajnik",
    "znajdź opakowanie herbaty",
    "zalej herbatę",
    "nalej wody do czajnika",
    "wyjmij kubek",
    "włóż herbatę do kubka"
]

order = {
    "nalej wody do czajnika": 1,
    "włącz czajnik": 2,
    "znajdź opakowanie herbaty": 3,
    "wyjmij kubek": 4,
    "włóż herbatę do kubka": 5,
    "zalej herbatę": 6
}

if __name__ == "__main__":
    # Zadanie 1
    print(name_dictionary)
    # Zadanie 2
    for i in range(-1,2):
        assert is_prime(i) == False, f"Only integers > 1 can be prime numbers"
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(100_001) == False

    primes = [num for num in nums if is_prime(num)]  # filter prime numbers from nums
    print(primes)

    # Zadanie 3
    for d in ['wt', 'czw', 'nie']:
        wk_days.append(d)
    print(wk_days)

    # Zadanie 3a
    wk_days.sort(key=lambda day: wk_days_dict[day])
    print(wk_days)

    # Zadanie 4
    instructions.sort(key=lambda step: order[step])  # find instruction ordinal number in `order` dictionary and use the number as sorting key
    print(instructions)
