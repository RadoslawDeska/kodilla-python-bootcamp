import business_cards
import datetime
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        duration = end - start
        print(f"Operation took {duration}.")
        return result
    return wrapper
    
@timeit
def create_contacts(cls, quantity):
    return business_cards.create_contacts(cls, quantity)

if __name__ == "__main__":
    pcards = create_contacts(business_cards.BaseContact, 1000)
    bcards = create_contacts(business_cards.BusinessContact, 1000)