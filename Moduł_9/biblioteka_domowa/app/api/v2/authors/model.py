from app.extensions.db import db


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    books = db.relationship(
        "Book", secondary="book_authors", back_populates="authors"
    )

    def __repr__(self):
        return f"<Author {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
        }
