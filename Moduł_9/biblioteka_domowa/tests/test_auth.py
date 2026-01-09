from app.extensions.db import db
from app.api.v2.users.model import User


def test_user_login(client):
    # create user
    u = User(email="john@black.com", password="black")
    db.session.add(u)
    db.session.commit()

    # login via web
    response = client.post("/login", data={
        "email": "john@black.com",
        "password": "black"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Logout" in response.data or b"Books" in response.data
