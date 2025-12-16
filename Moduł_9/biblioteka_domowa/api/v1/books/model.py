from typing import List, Optional
from extensions.db import db

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), unique=False, nullable=False)
    title = db.Column(db.String(255), unique=False, nullable=False)
    year = db.Column(db.Integer(), unique=False, nullable=False)
    pages = db.Column(db.Integer(), unique=False, nullable=False)
    publisher = db.Column(db.String(255), unique=False, nullable=True)
    
    # Get user id from `users` table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # set relation to the `users` table
    user = db.relationship("User", back_populates="books")

    def __init__(self, author: str, title: str, year: int, pages: int, publisher: str | None = None, user_id: int = 0):
        self.author = author
        self.title = title
        self.year = year
        self.pages = pages
        self.publisher = publisher
        self.user_id = user_id
    
    def __repr__(self):
        return f"<Book {self.author}, {self.title}, {self.year}, {self.publisher}>"
    
    @staticmethod
    def list_attrs():
        return ['id', 'author', 'title', 'year', 'pages', 'publisher']  # getmembers doesn't work outside app context
        
    @staticmethod
    def all_for_user(user_id: int) -> List["Book"]:
        return Book.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_for_user(user_id: int, key: int) -> Optional["Book"]:
        return Book.query.filter_by(user_id=user_id, id=key).first()
    
    @staticmethod
    def delete_for_user(user_id: int, key: int):
        out = Book.query.filter_by(id=key, user_id=user_id).delete()
        db.session.commit()
        return out  # 0 = no success
    
    def create(self):
        if not self.user_id:
            raise ValueError("user_id is required for creating a book")
        db.session.add(self)
        db.session.commit()
    
    def edit(self):
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "year": self.year,
            "pages": self.pages,
            "publisher": self.publisher,
        }
