# FastAPI Social Media API

A REST API built with FastAPI for a social-media-style app: users can register, log in, create posts, and vote (like) on posts.

## Features

- User registration and JWT-based authentication
- CRUD operations on posts, scoped to the authenticated owner
- Post voting (like/unlike) with vote counts included on post reads
- Post search, pagination (`limit`/`skip`), and filtering by title
- Database migrations managed with Alembic

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM with PostgreSQL (`psycopg2`)
- [Pydantic](https://docs.pydantic.dev/) / `pydantic-settings` for schemas and config
- [python-jose](https://github.com/mpdavis/python-jose) for JWTs, [passlib](https://passlib.readthedocs.io/)/`bcrypt` for password hashing
- [Alembic](https://alembic.sqlalchemy.org/) for schema migrations

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd FastAPI
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with the following (used by [app/config.py](app/config.py)):

```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## API Overview

| Method | Endpoint         | Description                          | Auth required |
|--------|------------------|---------------------------------------|----------------|
| POST   | `/users/`        | Create a new user                     | No             |
| GET    | `/users/{id}`    | Get a user by ID                      | No             |
| POST   | `/login`         | Log in and receive a JWT access token | No             |
| GET    | `/posts/`        | List posts (supports `search`, `limit`, `skip`) | Yes  |
| POST   | `/posts/`        | Create a post                         | Yes            |
| GET    | `/posts/{id}`    | Get a single post with vote count     | Yes            |
| PUT    | `/posts/{id}`    | Update a post you own                 | Yes            |
| DELETE | `/posts/{id}`    | Delete a post you own                 | Yes            |
| POST   | `/vote/`         | Like (`dir: 1`) or unlike (`dir: 0`) a post | Yes      |

Authenticated routes expect an `Authorization: Bearer <token>` header using the token returned from `/login`.

## Project Structure

```
app/
├── main.py          # App entrypoint, router registration, CORS
├── config.py         # Environment-based settings
├── database.py        # SQLAlchemy engine/session setup
├── models.py          # SQLAlchemy models (User, Post, Vote)
├── schemas.py          # Pydantic request/response schemas
├── oauth2.py           # JWT creation/validation, current-user dependency
├── utils.py             # Password hashing helpers
└── routers/
    ├── auth.py           # /login
    ├── user.py            # /users
    ├── mediaposts.py       # /posts
    └── vote.py             # /vote
```
