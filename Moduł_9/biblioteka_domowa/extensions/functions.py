from typing import Optional

from werkzeug.security import generate_password_hash

from .db import db
from .models import User


def get_user_by_email(email: Optional[str]):
    if not email:
        return None
    return User.query.filter_by(email=email).first()

def get_users() -> list[User]:
    return User.query.all()

def update_user_email(email: str, new_email: str):
    user = get_user_by_email(email)
    if user:
        if get_user_by_email(new_email):
            return None  # nie zdradzaj, że email jest zajęty
        user.email = new_email
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            return None
    return create_user(email, 'black')

def update_user_password(email: str, new_password: str):
    user = get_user_by_email(email)
    if user:
        user.password_hash = generate_password_hash(new_password)
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            return None
    return None

def create_user(email: str, password: str):
    if get_user_by_email(email):
        # użytkownik już istnieje
        return None
    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


