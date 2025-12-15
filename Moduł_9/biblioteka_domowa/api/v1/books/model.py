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

    def __init__(self, author: str, title: str, year: int, pages: int, publisher: str | None = None):
        self.author = author
        self.title = title
        self.year = year
        self.pages = pages
        self.publisher = publisher
    
    def __repr__(self):
        return f"<Book {self.author}, {self.title}, {self.year}, {self.publisher}>"
    
    @staticmethod
    def list_attrs():
        return ['id', 'author', 'title', 'year', 'pages', 'publisher']  # getmembers doesn't work outside app context
    
    @staticmethod
    def all() -> List["Book"]:
        return Book.query.all()
    
    @staticmethod
    def get(key: int) -> Optional["Book"]:
        return Book.query.get(key)
    
    @staticmethod
    def delete(key:int):
        out = Book.query.filter_by(id=key).delete()
        db.session.commit()
        return out  # 0 = no success
    
    def create(self):
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
