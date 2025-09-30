# CHEESE SHOP
prices_per_kilo = {
    'roquefort': 12.50,
    'stilton': 11.24,
    'brie': 9.30,
    'gouda': 8.55,
    'edam': 11.00,
    'parmezan': 16.50,
    'mozzarella': 14.00,
    'ser owczy': 122.32
}

# CLIENT
basket = {
    'roquefort': 1,  # cheese type, weight
    'stilton': 1,
    'brie': 1,
    'gouda': 1,
    'edam': 1,
    'parmezan': 1,
    'mozzarella': 1,
    'ser owczy': 1
}

# CHECKOUT
def scan_product(cheese, amount):
    return prices_per_kilo.get(cheese, None) * amount

def evaluate_basket(basket: dict):
    basket_total = 0
    basket_summary = {}
    
    for cheese, amount in basket.items():
        price = scan_product(cheese, amount)
        if price is not None:  # Evaluate only products in the shop's offer.
            basket_total += price
            basket_summary[cheese] = (amount, prices_per_kilo[cheese], price)
    
    return basket_summary, basket_total

def print_receit(basket: dict, decimal_point=","):
    if decimal_point not in [",", "."]:
        raise Exception("Invalid decimal point.")
    
    basket_summary, basket_total = evaluate_basket(basket)
    
    print("\n")
    print("#"*40)
    print("#","Paragon fiskalny".upper().center(36),"#")
    print("#","#",sep=" "*38)
    for cheese, (amount, price_per_kilo, price) in basket_summary.items():
        line = ''.join((
            "# ",
            f"{cheese}".ljust(13, " "),
            f"{amount:.3f}".rjust(6),
            "*",
            f"{price_per_kilo:.2f}".ljust(7),
            f"{price:.2f}".rjust(8),
            "#".rjust(3)))
        print(line.replace(".", decimal_point))
    
    print("#","#",sep=" "*38)
    print(''.join((
        "# Suma PLN",
        f"{basket_total}".rjust(len(line)-13), # 8 stands for length of left-most text
        "#".rjust(3))).replace(".", decimal_point))  
    print("#","#",sep=" "*38)
    print("#"*40)
    print("\n"*2)

print_receit(basket, decimal_point=",")