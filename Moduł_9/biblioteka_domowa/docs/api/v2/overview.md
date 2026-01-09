
# API v2 Overview

## Authentication

The API uses Bearer token authentication. Obtain a token by logging in, then include it in request headers:

```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Users

#### Login
**POST** `/api/v2/users/login`

Authenticate and receive a Bearer token.

```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response (200):**
```json
{
    "access_token": "eyJ...",
    "token_type": "Bearer"
}
```

#### Bootstrap Admin
**POST** `/api/v2/users/bootstrap-admin`

Create the first admin user (only works if no admin exists).

**Headers:**
```
X-Bootstrap-Secret: <FLASK_BIBLIOTEKA_DOMOWA_API_ADMIN_SECRET_KEY>
```

**Body:**
```json
{
    "email": "admin@example.com",
    "password": "securepassword"
}
```

#### Register User
**POST** `/api/v2/users/register`

Register a new user (admin only).

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Body:**
```json
{
    "email": "newuser@example.com",
    "password": "password123",
    "role": "user"
}
```

### Books

#### List Books
**GET** `/api/v2/books/`

Retrieve all books for the authenticated user.

**Response (200):**
```json
[
    {
        "id": 1,
        "author": "John Doe",
        "title": "Sample Book",
        "year": 2020,
        "pages": 350,
        "publisher": "Publisher Name"
    }
]
```

#### Create Book
**POST** `/api/v2/books/`

Add a new book to the library.

**Body:**
```json
{
    "author": "Jane Smith",
    "title": "New Book",
    "year": 2023,
    "pages": 400,
    "publisher": "Publisher"
}
```

#### Get Book
**GET** `/api/v2/books/<book_id>`

Retrieve a specific book by ID.

#### Update Book
**PATCH/PUT** `/api/v2/books/<book_id>`

Update book details (partial or full update).

**Body:**
```json
{
    "title": "Updated Title",
    "pages": 450
}
```

#### Delete Book
**DELETE** `/api/v2/books/<book_id>`

Remove a book from the library.

**Response (200):**
```json
{
    "deleted": true,
    "id": 1
}
```

## Error Responses

- **400** Bad Request
- **401** Unauthorized (missing/invalid token)
- **403** Forbidden (insufficient permissions)
- **404** Not Found
- **409** Conflict (email already registered)
