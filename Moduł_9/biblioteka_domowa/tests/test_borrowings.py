from app.api.v2.authors.model import Author
from app.api.v2.books.model import Book
from app.api.v2.users.model import User
from app.extensions.db import db


def auth_headers(client):
    u = User(email="john@black.com", password="black")
    db.session.add(u)
    db.session.commit()

    client.post("/login", data={"email": "john@black.com", "password": "black"})

    return {"Content-Type": "application/json"}


def setup_book():
    a = Author(name="Tolkien")
    db.session.add(a)
    db.session.commit()

    b = Book(
        title="The Hobbit",
        year=1937,
        pages=310,
        publisher="Allen & Unwin",
        user_id=1,
        authors=[a],
    )
    db.session.add(b)
    db.session.commit()
    return b


def test_borrow_and_return(client, auth_headers):
    book = setup_book()

    # borrow
    borrow = client.post(
        f"/api/v2/borrowings/{book.id}/borrow",
        json={"borrower_name": "Jan Kowalski"},
        headers=auth_headers,
    )

    assert borrow.status_code == 201

    # return
    ret = client.post(f"/api/v2/borrowings/{book.id}/return", headers=auth_headers)
    assert ret.status_code == 200
    assert ret.json["returned_at"] is not None
