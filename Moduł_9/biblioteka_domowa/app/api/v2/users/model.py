import enum
from typing import List, Optional

from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions.db import db

class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)

    books = db.relationship("Book", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email: str, password: str, role: RoleEnum = RoleEnum.user):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    @staticmethod
    def get_users() -> List["User"]:
        return User.query.all()

    @classmethod
    def get_by_email(cls, email: Optional[str]) -> Optional["User"]:
        if not email:
            return None
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_user(cls, email: str, password: str) -> Optional["User"]:
        if cls.get_by_email(email):
            # user exists
            return None
        user = cls(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def update_email(self, new_email: str) -> bool:
        if User.get_by_email(new_email):
            return False
        self.email = new_email
        db.session.commit()
        return True

    def update_password(self, new_password: str) -> bool:
        self.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return True

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def modify(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.email}>"
