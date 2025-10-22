def is_palindrome(text: str) -> bool:
    """
    Check if the given text is a palindrome.
    A palindrome reads the same forwards and backwards, ignoring case.
    
    With this implementation, spaces and punctuation are ignored.

    Args:
        text (str): The text to check. Can include letters, numbers, spaces, and punctuation.\\
        Expects string input, but will convert other types to string if possible.
    Returns:
        bool: True if the text is a palindrome, False otherwise.
    """
    try:
        text = str(text)  # Ensure the input is a string
    except Exception:
        print("Cannot convert input to string.")
        return False  # If conversion fails, return False
    text = ''.join(char for char in text if char.isalnum())  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase to ensure case insensitivity

    return text == text[::-1]  # Check if the text is the same as its reverse

if __name__ == "__main__":
    # Positive cases
    assert is_palindrome(121)
    assert is_palindrome(1.21)
    assert is_palindrome([1,2.2,1])
    assert is_palindrome("")
    assert is_palindrome("A")
    assert is_palindrome("Radar")
    assert is_palindrome("Tolo ma samolot")
    assert is_palindrome("Kobyła ma mały bok")
    assert is_palindrome("A123 ,321A")
    # False cases
    assert is_palindrome([1,2.1,1]) is False
    assert is_palindrome("Był sobie król") is False