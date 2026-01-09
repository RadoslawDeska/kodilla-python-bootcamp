# Biblioteka Domowa (Home Library)

A Flask-based REST API and web application for managing a personal book library with user authentication and role-based access control.

## Features

- **User Authentication**: Web and API-based login with JWT tokens
- **Role-Based Access Control**: Admin and user roles with different permissions
- **Book Management**: Create, read, update, and delete books in your personal library
- **API v2**: RESTful API endpoints for programmatic access
- **File Upload**: Support for image uploads with validation (PNG, JPG, GIF)
- **Database**: SQLite with SQLAlchemy ORM
- **Bootstrap Admin**: Initialize first admin user with secret key


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RadoslawDeska/biblioteka_domowa.git
   cd biblioteka_domowa

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Set up the environment:** Follow the instructions in the Environment Configuration section.

## Environment Configuration

To configure the application, you need to set up the environment variables. Follow these steps to edit the `example.env` file:

1. **Locate the `example.env` file**: This file is located in the root directory of your project.
2. **Copy the `example.env` file**: Create a copy of the `example.env` file and rename it to `.env`. This file will be used to store your environment variables.
3. **Edit the `.env` file**: Open the `.env` file in a text editor and set the variables contained within:

    ```bash
    FLASK_BIBLIOTEKA_DOMOWA_SECRET_KEY  # Your very secretive password to encrypt the Flask session

    FLASK_BIBLIOTEKA_DOMOWA_DB  # Full path to where database should be located

    FLASK_BIBLIOTEKA_DOMOWA_API_ADMIN_SECRET_KEY  # Set your very secretive password to the API.

## Usage
1. **Run the application** (from the project root, where wsgi.py is located):
    ```bash
    flask run
    ```

2. **Access the web application:**
    
    Open your browser and go to `http://127.0.0.1:5000`.

3. **API access:**

    All REST API v2 endpoints are available under `app/api/v2/`

4. **Admin bootstrap (optional):**
    
    If no users exist, you can initialize the first admin user by providing the secret key defined in your .env file.

## 📦 Database Migrations (Flask‑Migrate / Alembic)

The application uses Flask‑Migrate (Alembic) to manage database schema changes.
This ensures your database structure is versioned, reproducible, and safely upgradable without manually editing SQLite files.

0. **Initialize migrations (only once)**
    ```bash
    flask db init
    ```
1. **Generate a new migration after modifying models**
    ```bash
    flask db migrate -m "describe your changes" 
    ```
2. **Apply migrations**
    ```bash
    flask db upgrade
    ```
3. **Rollback the last migration**
    ```bash
    flask db downgrade
    ```
    ⚠️ **Important:** Never edit app.db manually. Always use migrations to apply structural changes.


## 🗂️ Project Structure

The project follows a modular, scalable architecture based on Flask blueprints.

Each feature (books, authors, borrowings, users) is isolated into its own package with separate models, validation schemas, and view controllers.

```
biblioteka_domowa/
│
├── app/
│   ├── api/
│   │   └── v2/
│   │       ├── authors/
│   │       │   ├── model.py            # SQLAlchemy models
│   │       │   ├── validation.py       # Pydantic request/response schemas
│   │       │   └── views.py            # Blueprint routes (CRUD)
│   │       ├── books/
│   │       │   ├── model.py
│   │       │   ├── validation.py
│   │       │   └── views.py
│   │       ├── borrowings/
│   │       │   ├── model.py
│   │       │   ├── validation.py
│   │       │   └── views.py
│   │       └── users/
│   │           ├── model.py
│   │           ├── validation.py
│   │           └── views.py
│   │
│   ├── extensions/
│   │   └── db.py                       # SQLAlchemy initialization
│   │
│   ├── templates/                      # Jinja2 templates for the web UI
│   ├── static/                         # CSS, JS, images
│   ├── error_handling.py               # Centralized error handlers
│   ├── routes.py                       # Web routes (non‑API)
│   └── __init__.py                     # create_app() factory
│
├── migrations/                         # Alembic migration scripts
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py                     # Pytest fixtures
│   ├── test_auth.py                    # Authentication tests
│   ├── test_books.py                   # Book management tests
│   ├── test_users.py                   # User management tests
│   └── test_borrowings.py              # Borrowing management tests
|
├── wsgi.py                             # Entry point for Flask / WSGI servers
├── requirements.txt
├── example.env
└── README.md
```
