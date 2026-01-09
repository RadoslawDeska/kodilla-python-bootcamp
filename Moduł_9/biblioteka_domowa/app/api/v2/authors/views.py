from flask import Blueprint, jsonify, request, abort
from pydantic import ValidationError
from flask import g

from app.api.v2.books.model import Author
from .validation import (
    AuthorCreateSchema,
    AuthorUpdateSchema,
    AuthorResponseSchema,
)
from app.auth import api_login_required
from app.extensions.db import db

authors_bp = Blueprint("authors", __name__, url_prefix="/api/v2/authors")


@authors_bp.route("/", methods=["GET"])
@api_login_required
def list_authors():
    authors = Author.query.all()
    return jsonify([a.to_dict() for a in authors])


@authors_bp.route("/", methods=["POST"])
@api_login_required
def create_author():
    try:
        data = AuthorCreateSchema.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    author = Author(name=data.name, bio=data.bio)
    db.session.add(author)
    db.session.commit()

    return jsonify(AuthorResponseSchema.model_validate(author.to_dict()).model_dump()), 201


@authors_bp.route("/<int:author_id>", methods=["GET"])
@api_login_required
def get_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        abort(404)
    return jsonify(author.to_dict())


@authors_bp.route("/<int:author_id>", methods=["PATCH", "PUT"])
@api_login_required
def update_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        abort(404)

    try:
        data = AuthorUpdateSchema.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)

    db.session.commit()
    return jsonify(author.to_dict())


@authors_bp.route("/<int:author_id>", methods=["DELETE"])
@api_login_required
def delete_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        abort(404)

    db.session.delete(author)
    db.session.commit()
    return jsonify({"deleted": True, "id": author_id})
