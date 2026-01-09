from app.extensions.db import db
from app.api.v2.users.model import User


def auth_headers(client):
    # login user
    u = User(email="john@black.com", password="black")
    db.session.add(u)
    db.session.commit()

    client.post("/login", data={
        "email": "john@black.com",
        "password": "black"
    })

    return {"Content-Type": "application/json"}


def test_create_author(client, auth_headers):
    response = client.post("/api/v2/authors/", json={
        "name": "J.R.R. Tolkien",
        "bio": "Oxford professor"
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json["name"] == "J.R.R. Tolkien"


def test_list_authors(client, auth_headers):
    client.post("/api/v2/authors/", json={
        "name": "Author A"
    }, headers=auth_headers)

    response = client.get("/api/v2/authors/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) == 1
