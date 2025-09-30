# CHEESE SHOP
prices_per_kilo = {
    'roquefort': 12.50,
    'stilton': 11.24,
    'brie': 9.30,
    'gouda': 8.55,
    'edam': 11.00,
    'parmezan': 16.50,
    'mozzarella': 14.00,
    'ser owczy': 122.32,
    'listek mięty': 100
}

# CLIENT
basket = {
    'roquefort': 2,  # cheese type, weight
    'stilton': 1,
    'brie': 1,
    'gouda': 1,
    'edam': 1,
    'parmezan': 3.5,
    'mozzarella': 1.30,
    'ser owczy': 2.20,
    'listek mięty': 0.2
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
    
    print("Raport z zakupów:")
    for product, (amount, _, price) in basket_summary.items():
        line = '\t'.join((product,
                    f"{amount:.3f} kg",
                    f"{price:.2f} zł"))
        print(line.replace(".",decimal_point))
    print(f"Suma zł: {basket_total:.2f}".replace(".",decimal_point))

print_receit(basket, decimal_point=",")