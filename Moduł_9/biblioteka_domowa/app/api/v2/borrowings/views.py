from flask import Blueprint, jsonify, request, abort
from pydantic import ValidationError
from flask import g
from datetime import datetime

from app.api.v2.books.model import Book, Borrowing
from .validation import BorrowCreateSchema
from app.extensions.db import db
from app.auth import api_login_required

borrow_bp = Blueprint("borrow", __name__, url_prefix="/api/v2/borrowings")


@borrow_bp.route("/", methods=["GET"])
@api_login_required
def list_borrowings():
    borrows = Borrowing.query.all()
    return jsonify([b.to_dict() for b in borrows])


@borrow_bp.route("/<int:book_id>/borrow", methods=["POST"])
@api_login_required
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)

    if not book.is_on_shelf:
        return jsonify({"error": "Book already borrowed"}), 409

    try:
        data = BorrowCreateSchema.model_validate(request.json or {})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    borrowing = Borrowing(
        book_id=book.id,
        user_id=g.api_user_id,
        borrower_name=data.borrower_name,
        due_date=datetime.fromisoformat(data.due_date) if data.due_date else None,
    )

    book.is_on_shelf = False
    db.session.add(borrowing)
    db.session.commit()

    return jsonify(borrowing.to_dict()), 201


@borrow_bp.route("/<int:book_id>/return", methods=["POST"])
@api_login_required
def return_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)

    if book.is_on_shelf:
        return jsonify({"error": "Book is not borrowed"}), 409

    borrowing = Borrowing.query.filter_by(book_id=book_id, returned_at=None).first()
    if not borrowing:
        abort(404)

    borrowing.returned_at = datetime.utcnow()
    book.is_on_shelf = True
    db.session.commit()

    return jsonify(borrowing.to_dict())
