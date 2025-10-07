# CHEESE SHOP
from pathlib import Path


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

def generate_receipt(basket: dict, max_len: int):
    """Generate receipt lines using yield for easy testing line by line."""
    # Fixed widths for amount and price
    amount_width = 8
    price_width = 8
    units = " kg "
    currency = " zł"
    summary = "Suma zł: "

    # Calculate product name width
    fixed_width = amount_width + len(units) + price_width + len(currency)
    prod_width = max_len - fixed_width
    if prod_width <= 0:
        raise Exception(f"max_len is too small to format the receipt. Try at least {fixed_width + 1}")
    
    basket_summary, basket_total = evaluate_basket(basket)
    for product, (amount, _, price) in basket_summary.items():
        # Format the line to fit the max_len
        # Cut the product name if needed
        product = product[:prod_width]
        line = f"{product:<{prod_width}}{amount:>{amount_width}.3f}{units}{price:>{price_width}.2f}{currency}"
        yield line
    yield f"{summary}{basket_total:>{max_len - len(summary)}.2f}"

def format_receipt(basket: dict, decimal_point=",", max_len=40):
    if decimal_point not in [",", "."]:
        raise Exception("Invalid decimal point.")
    
    lines = ["Raport z zakupów:"]
    for line in generate_receipt(basket, max_len=max_len):
        lines.append(line.replace(".", decimal_point))
    
    return lines

def receipt_to_string(lines) -> str:
    return "\n".join(lines)

def print_receipt(basket: dict, decimal_point=",", max_len=40):
    """Print the receipt to the console."""
    receipt = format_receipt(basket, decimal_point, max_len)
    print(receipt_to_string(receipt))

def save_receipt_to_file(basket: dict, directory = Path(__file__).parent, decimal_point=",", max_len=40):
    """Save the receipt to a text file if you want to send it or print later.
    
    By default, the file is saved in the same directory as this script.
    """
    file = directory / "receipt.txt"
    with open(file, 'w', encoding="utf-8") as f:
        receipt = format_receipt(basket, decimal_point, max_len)
        f.write(receipt_to_string(receipt))

def test_generate_receipt(basket, max_len=40):
    """Test if all lines in the receipt have length equal to max_len.
    It means that the formatting is correct, i.e. each line spans the max_len width.
    """
    function_to_test = generate_receipt
    receipt = generate_receipt(basket, max_len=max_len)
    test_positive = True
    
    for i, line in enumerate(receipt):
        try:
            assert len(line) == max_len
        except AssertionError:
            if not test_positive:
                print(f"\nFunction {function_to_test.__name__} failed. Details:")
            print(f"Linia {i+1} ma niepoprawną długość: {len(line)}")
            print(f"`{line}`")
            test_positive = False
    
    return test_positive

if __name__ == "__main__":
    receipt_width = 30

    # Run test and print receipt only if test passed
    if test_generate_receipt(basket, max_len=receipt_width):
        print_receipt(basket, decimal_point=",", max_len=receipt_width)
        save_receipt_to_file(basket, max_len=receipt_width)