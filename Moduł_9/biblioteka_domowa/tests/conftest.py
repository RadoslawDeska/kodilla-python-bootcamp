import pytest
from app import create_app
from app.extensions.db import db
from app.api.v2.users.model import User
from app.api.v2.authors.model import Author
from app.api.v2.books.model import Book


@pytest.fixture
def client():
    app = create_app(testing=True)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

@pytest.fixture
def auth_headers(client):
    u = User(email="test@example.com", password="testpassword")
    db.session.add(u)
    db.session.commit()

    response = client.post("/api/v2/users/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200, f"Login failed: {response.status_code}"

    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}



def setup_book():
    """Helper to create a book for borrowing tests."""
    author = Author(name="Test Author")
    db.session.add(author)
    db.session.commit()

    book = Book(
        title="Test Book",
        year=2020,
        pages=200,
        publisher="Test Publisher"
    )
    book.authors.append(author)
    db.session.add(book)
    db.session.commit()

    return book