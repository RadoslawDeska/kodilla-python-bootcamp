from flask import Blueprint, jsonify, abort, request, session
from pydantic import ValidationError

from api.v1.books.validation import BookCreateSchema, BookResponseSchema, BookUpdateSchema
from .model import Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

def validate_book_access(bk: Book|None):
    if not bk:
        abort(404)
    if bk.user_id != session["user_id"]:
        abort(403)
    return bk

@books_bp.before_request                # this makes every request
def require_login():                    # require logged-in state
    if not session.get("logged_in"):    # to access the methods
        abort(403)

@books_bp.route("/", methods=["GET"])
def books_list_api_v1():
    books = Book.all_for_user(session["user_id"])
    return jsonify([b.to_dict() for b in books])

@books_bp.route("/", methods=["POST"])
def create_book():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        data = BookCreateSchema.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    new_book = Book(
        author=data.author,
        title=data.title,
        year=data.year,
        pages=data.pages,
        publisher=data.publisher,
        user_id=session["user_id"]
        )
    new_book.create()  # update database
    return jsonify(BookResponseSchema.model_validate(new_book.to_dict()).model_dump()), 201


## PER ID VIEWS
@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.get_for_user(session["user_id"], book_id)
    book = validate_book_access(book)
    return jsonify(book.to_dict())

@books_bp.route("/<int:book_id>", methods=["PATCH", "PUT"])
def edit_book(book_id):
    book = Book.get_for_user(session["user_id"], book_id)
    book = validate_book_access(book)
    try:
        data = BookUpdateSchema.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # update fields from request
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    book.edit()  # update database
    return jsonify(BookResponseSchema.model_validate(book.__dict__).model_dump()), 200

@books_bp.route("/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    book = Book.get_for_user(session["user_id"], book_id)
    book = validate_book_access(book)
    
    result = Book.delete_for_user(session["user_id"], book_id)
    if not result:
        abort(404)
    return jsonify({"deleted": True, "id": book_id})

