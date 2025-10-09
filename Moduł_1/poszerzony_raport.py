# CHEESE SHOP
from pathlib import Path

class InvalidArgument(Exception):
    pass

offer = {
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
    'listek mięty': 0.2,
    'ptasia kupa': 1,
}

# FUNKCJE OBLICZAJĄCE
def _product_price2pay(product_name, amount:float|int) -> float|None:
    """Calculate product price for given amount.

    Args:
        product_name (string): Product name
        amount (float|int): Product amount (kg|#items)

    Returns:
        float|None: Price for given amount. None when the product doesn't exist in the shop's `offer`
    """
    if amount <= 0:
        raise Exception("Product amount cannot be zero or less.")
    price = offer.get(product_name, None)
    if price is None:
        return None
    return price * amount

def _evaluate_basket(basket: dict[str, float|int]) -> tuple[dict, float]:
    """Evaluate the basket contents and its total price.

    Args:
        basket (dict[str, float|int]): Basket contents in the format {product_name: amount}

    Returns:
        tuple[dict, float]: Valid basket contents and total price
    """
    basket_total = 0
    basket_summary = {}
    
    for product_name, amount in basket.items():
        price = _product_price2pay(product_name, amount)
        if price is not None:  # Evaluate only products in the shop's offer.
            basket_summary[product_name] = (amount, offer[product_name], float(price))
            basket_total += price
    
    return basket_summary, basket_total

# FUNKCJE FORMATUJĄCE
def _format_column(coltype: str, column_content, width: int, decimal_point=".") -> str:
    """Format a single column_content of type `coltype` to fit the given width.
    
    Args:
        coltype (str): Type of the column. One of "product", "amount", "price"
        column_content (str|float|int): Content to format
        width (int): Width of the column
        decimal_point (str, optional): Decimal point character. Defaults to ".".
    Returns:
        str: Formatted column content
    """
    def _trim(s: str, max_length: int) -> str:
        return s[:max_length]
    def _align_fill(s: str, width: int, align: str) -> str:
        return f"{s:{align}{width}}"

    if any([arg is None for arg in [coltype, column_content, width, decimal_point]]):
        raise InvalidArgument("NoneType is not allowed as any of the arguments.")
    
    if coltype in ["amount", "price"]:
        if not isinstance(column_content, (float, int)):
            raise InvalidArgument(f"{str(coltype).capitalize()} must be a number. Check the coltype argument, and next the basket contents.")

        align = ">"    
        digits = 2 if coltype == "price" else 3 # 1 gram precision (for weights); for items it will be .000; price will be 2 decimal places
        column_content = f"{float(column_content):.{digits}f}"
    elif coltype == "product":
        column_content = str(column_content)  # Convert to string if required
        align = "<"
    else:
        raise InvalidArgument("Invalid column type. Use 'product', 'amount' or 'price'.")

    # Adjust the column width and align
    column_content = _trim(column_content, width)
    column_content = _align_fill(column_content, width, align)

    # Format decimal point
    if coltype in ["amount", "price"] and decimal_point != ".":
        column_content = column_content.replace(".", decimal_point)
    
    return column_content

def _products_listing(basket: dict, max_width: int, decimal_point="."):
    """Generate lines to print on the receipt with aligned formatting.\n
    The function returns generator for immediate printing and for easy testing line by line.
    
    Args:
        basket (dict[str, float|int]): Basket contents in the format {product_name: amount}

    Returns:
        tuple[dict, float]: Valid basket contents and total price
    
    """
    # Fixed widths for amount and price
    amount_width = 8
    price_width = 8
    UNITS = " kg "
    CURRENCY = " zł"
    SUMMARY = "Suma zł: "
    MIN_PROD_WIDTH = 5

    # Calculate product name width in the generated line
    fixed_width = amount_width + len(UNITS) + price_width + len(CURRENCY)
    prod_width = max_width - fixed_width
    # Define minimum width of the product name on the receipt
    if prod_width < MIN_PROD_WIDTH:
        raise Exception(f"max_width is too small to format the receipt. Try at least {fixed_width + MIN_PROD_WIDTH}")
    
    yield "Raport z zakupów:"
    basket_summary, basket_total = _evaluate_basket(basket)
    for product, (amount, _, price) in basket_summary.items():
        # Format the line to fit the max_width
        
        product = _format_column("product", product, prod_width)
        amount = _format_column("amount",
                                amount,
                                amount_width,
                                decimal_point=decimal_point
                                )
        price = _format_column("price",
                               price,
                               price_width,
                               decimal_point=decimal_point
                               )
        yield f"{product}{amount}{UNITS}{price}{CURRENCY}"
    
    basket_total = _format_column("price",
                                  basket_total,
                                  max_width - len(SUMMARY),
                                  decimal_point=decimal_point
                                  )
    yield f"{SUMMARY}{basket_total}"

def _format_receipt(basket: dict, decimal_point=",", max_width=40):
    """Format the receipt for valid `basket`.\n
    Set maximum line width (`max_width`) and `decimal_point` for numbers formatting.
    """
    if decimal_point not in [",", "."]:
        raise Exception("Invalid decimal point.")
    
    lines = ["Raport z zakupów:"]
    for line in _products_listing(basket, max_width=max_width):
        lines.append(line.replace(".", decimal_point))
    
    return lines

def receipt_to_string(lines) -> str:
    return "\n".join(lines)

def print_receipt(basket: dict, decimal_point=",", max_width=40):
    """Print the receipt to the console."""
    receipt = _format_receipt(basket, decimal_point, max_width)
    print(receipt_to_string(receipt))

def save_receipt_to_file(basket: dict, directory = Path(__file__).parent, decimal_point=",", max_width=40):
    """Save the receipt to a text file if you want to send it or print later.
    
    By default, the file is saved in the same directory as this script.
    """
    file = directory / "receipt.txt"
    with open(file, 'w', encoding="utf-8") as f:
        receipt = _format_receipt(basket, decimal_point, max_width)
        f.write(receipt_to_string(receipt))

def test_products_listing(basket, max_width=40):
    """Test if all lines in the receipt have length equal to max_width.
    It means that the formatting is correct, i.e. each line spans the max_width width.
    """
    function_to_test = _products_listing
    receipt = _products_listing(basket, max_width=max_width)
    test_positive = True
    
    for i, line in enumerate(receipt):
        try:
            assert len(line) == max_width
        except AssertionError:
            if not test_positive:
                print(f"\nFunction {function_to_test.__name__} failed. Details:")
            print(f"Linia {i+1} ma niepoprawną długość: {len(line)}")
            print(f"`{line}`")
            test_positive = False
    
    return test_positive

if __name__ == "__main__":
    # TESTUJ
    
    # TEST OFERTY
    # Czy oferta ma dodatnie wartości?
    assert all([i>0 for i in offer.values()]), "Niektóre produkty w `offer` mają cenę 0 lub mniej"
    
    # TEST OBLICZANIA CENY PRODUKTU
    # Czy cena jest obliczana poprawnie?
    assert _product_price2pay(product_name = "brie", amount=1) == 9.3, "Cena obliczana niepoprawnie"
    # Czy nieistniejące produkty są zwracane jako None
    assert _product_price2pay(product_name = "ufoludek", amount=1) is None
    
    # TEST WERYFIKACJI KOSZYKA
    # Czy cena jest floatem?
    assert isinstance(_evaluate_basket(basket)[1], float), "Cena nie jest floatem"
    # Czy koszyk końcowy (po walidacji) zawiera tylko produkty z oferty?
    assert all([k in offer.keys() for k in _evaluate_basket(basket)[0].keys()]), "Niektóre produkty nie istnieją w ofercie"
    # Czy cena końcowa jest dodatnia?
    assert _evaluate_basket(basket)[1] > 0, "Cena jest ujemna"
    
    # Czy _format_column przyjmuje różne typy danych i formatuje je poprawnie?
    assert _format_column("product", "test", 5) == "test "
    assert _format_column("product", 1, 5) == "1    "
    assert _format_column("product", 123.4567, 4) == "123."
    
    # Czy _format_column zwraca string lub podnosi wyjątek InvalidArgument przy niepoprawnych danych?
    for test_coltype in ["product", "amount", "price", "invalid"]:
        for test_value in [None, "test", 123, 123.456]:
            print(f"Checking {test_coltype} - {test_value} pair")
            if test_coltype == "invalid":
                try:
                    _format_column(test_coltype, test_value, 5)
                except Exception as e:
                    assert isinstance(e, InvalidArgument)
            else:
                try:
                    assert isinstance(_format_column(test_coltype, test_value, 5), str)
                    assert len(_format_column(test_coltype, test_value, 5)) == 5
                except Exception as e:
                    assert isinstance(e, InvalidArgument)

    # TEST FORMATOWANIA PARAGONU
    receipt_width = 28
    test_products_listing(basket, max_width=receipt_width)
    # print_receipt(basket, decimal_point=",", max_width=receipt_width)
    # save_receipt_to_file(basket, max_width=receipt_width)