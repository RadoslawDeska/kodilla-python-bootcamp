from app.api.v2.authors.model import Author
from app.api.v2.users.model import User
from app.extensions.db import db


def auth_headers(client):
    u = User(email="john@black.com", password="black")
    db.session.add(u)
    db.session.commit()

    client.post("/login", data={"email": "john@black.com", "password": "black"})

    return {"Content-Type": "application/json"}


def test_create_book_with_author(client, auth_headers):
    # create author
    a = Author(name="Tolkien")
    db.session.add(a)
    db.session.commit()

    response = client.post(
        "/api/v2/books/",
        json={
            "title": "The Hobbit",
            "year": 1937,
            "pages": 310,
            "publisher": "Allen & Unwin",
            "author_ids": [a.id],
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json["title"] == "The Hobbit"
    assert len(response.json["authors"]) == 1


def test_update_book(client, auth_headers):
    a = Author(name="Tolkien")
    db.session.add(a)
    db.session.commit()

    # create book
    book = client.post(
        "/api/v2/books/",
        json={
            "title": "Book",
            "year": 2000,
            "pages": 100,
            "author_ids": [a.id],
        },
        headers=auth_headers,
    ).json

    # update
    response = client.patch(
        f"/api/v2/books/{book['id']}",
        json={"title": "Updated Book"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json["title"] == "Updated Book"
