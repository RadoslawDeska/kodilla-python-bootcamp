import csv
import json
from decimal import Decimal

import requests


def write_csv(path, data, fieldnames=None, delimiter=",") -> tuple[bool, None]:
    '''Write CSV file given the path, fieldnames and data'''
    if fieldnames is None:
        fieldnames = data[0].keys()
    
    try:
        with open(path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        print(f"Permission to write is required for {path}.")
        return False, None
    except IsADirectoryError:
        print(f"Not a file: {path}.")
        return False, None
    except OSError as e:
        print(f"OS Error occurred: {e}")
        return False, None
    else:
        return True, None

def read_csv(path, delimiter=","):
    """Read CSV file and return success/error boolean and the list of `Item`s."""
    # Read the CSV file
    try:
        dicts = []
        with open(path, "r", newline='') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                dicts.append(row)
        return dicts
        
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error reading {path}: {e}")
        return

def get_json_text() -> list:
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    return response.text  # text instead of json() for exact numbers

def parse_text(text) -> dict:
    return json.loads(text, parse_float=Decimal)[0]