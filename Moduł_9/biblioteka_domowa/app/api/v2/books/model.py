from typing import List, Optional, Iterable, cast
from datetime import datetime, timezone

from app.extensions.db import db


# Association table for many-to-many Book <-> Author
book_authors = db.Table(
    'book_authors',
    db.Column(
        'book_id',
        db.Integer,
        db.ForeignKey('books.id', name='fk_book_authors_book_id'),
        primary_key=True
    ),
    db.Column(
        'author_id',
        db.Integer,
        db.ForeignKey('authors.id', name='fk_book_authors_author_id'),
        primary_key=True
    ),
)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    books = db.relationship('Book', secondary=book_authors, back_populates='authors')

    def __repr__(self):
        return f"<Author {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
        }


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    year = db.Column(db.Integer(), unique=False, nullable=False)
    pages = db.Column(db.Integer(), unique=False, nullable=False)
    publisher = db.Column(db.String(255), unique=False, nullable=True)
    is_on_shelf = db.Column(db.Boolean(), default=True, nullable=False)

    # FK to users
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_books_user_id"),
        nullable=False
    )
    user = db.relationship("User", back_populates="books")

    authors = db.relationship('Author', secondary=book_authors, back_populates='books')

    def __init__(self, title: str, year: int, pages: int, publisher: str | None = None, user_id: int = 0, authors: Optional[List[Author]] = None):
        self.title = title
        self.year = year
        self.pages = pages
        self.publisher = publisher
        self.user_id = user_id
        if authors:
            self.authors = authors

    def __repr__(self):
        return f"<Book {self.title} ({self.year})>"

    @staticmethod
    def list_attrs():
        return ['id', 'title', 'year', 'pages', 'publisher', 'is_on_shelf']

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
        return out

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
            "title": self.title,
            "year": self.year,
            "pages": self.pages,
            "publisher": self.publisher,
            "is_on_shelf": bool(self.is_on_shelf),
            "authors": [a.to_dict() for a in cast(Iterable, self.authors)],
        }


class Borrowing(db.Model):
    __tablename__ = 'borrowings'
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', name='fk_borrowings_book_id'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', name='fk_borrowings_user_id'),
        nullable=True
    )

    borrower_name = db.Column(db.String(255), nullable=True)
    borrowed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)

    book = db.relationship('Book', backref=db.backref('borrowings', lazy='dynamic'))

    def __repr__(self):
        who = self.borrower_name or f'user:{self.user_id}'
        return f"<Borrowing {self.book_id} by {who}>"

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'borrower_name': self.borrower_name,
            'borrowed_at': self.borrowed_at.isoformat() if self.borrowed_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
        }
