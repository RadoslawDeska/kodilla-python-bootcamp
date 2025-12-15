from functools import wraps
from flask import abort, session

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # sprawdzenie sesji
        if not session.get("logged_in"):
            abort(401)
        return f(*args, **kwargs)
    return wrapper