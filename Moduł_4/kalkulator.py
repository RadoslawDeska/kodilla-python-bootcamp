import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

action = input("Podaj działanie, posługując się odpowiednią liczbą:\n1 Dodawanie\n2 Odejmowanie\n3 Mnożenie\n4 Dzielenie\n>>> ")

while True:
    match action:
        case "1" | "2" | "3" | "4":
            break
        case _:
            logging.warning("Wybierz liczbę między 1 i 4.")
            action = input(">>> ")

numbers = []

def get_number(i):
    if i <= 2:
        inp = input(f"Podaj {i}. liczbę >>> ")
    if i > 2:
        inp = input(f"Podaj {i}. liczbę lub wciśnij [Enter], aby obliczyć >>> ")
    try:
        num = float(inp)
    except ValueError:
        return None
    else:
        return num
    
i = 1
while True:
    if action == "2" or action == "4":  # stop collecting numbers after 2 operands
        if len(numbers) == 2:
            break
    
    num = get_number(i)
    if num:
        numbers.append(num)
        i += 1
    else:
        if action == "1" or action == "3":
            if len(numbers) > 1:
                break
            else:
                logging.warning("Wymagane są przynajmniej dwie liczby.")
        else:
            logging.warning("Wymagane są dwie liczby.")


list_of_numbers = ", ".join([str(i) for i in numbers[:-1]])
list_of_numbers += f" i {numbers[-1]}"

result = numbers[0]
        
match action:
    case "1":
        logging.info(f"Dodaję {list_of_numbers}")
        for i in numbers[1:]:
            result += i
    case "2":
        logging.info(f"Odejmuję {list_of_numbers}")
        for i in numbers[1:]:
            result -= i
    case "3":
        logging.info(f"Mnożę {list_of_numbers}")
        for i in numbers[1:]:
            result *= i
    case "4":
        logging.info(f"Dzielę {list_of_numbers}")
        for i in numbers[1:]:
            result /= i
    
logging.info(f"Wynik to {result}")