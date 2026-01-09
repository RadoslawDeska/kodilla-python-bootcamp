from datetime import datetime, timezone

from app.extensions.db import db


class Borrowing(db.Model):
    __tablename__ = "borrowings"
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id", name="fk_borrowings_book_id"),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_borrowings_user_id"),
        nullable=True,
    )

    borrower_name = db.Column(db.String(255), nullable=True)
    borrowed_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    due_date = db.Column(db.DateTime, nullable=True)
    returned_at = db.Column(db.DateTime, nullable=True)

    book = db.relationship(
        "Book", backref=db.backref("borrowings", lazy="dynamic")
    )

    def __repr__(self):
        who = self.borrower_name or f"user:{self.user_id}"
        return f"<Borrowing {self.book_id} by {who}>"

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "borrower_name": self.borrower_name,
            "borrowed_at": self.borrowed_at.isoformat()
            if self.borrowed_at
            else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "returned_at": self.returned_at.isoformat()
            if self.returned_at
            else None,
        }
