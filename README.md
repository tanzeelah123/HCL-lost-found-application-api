## Lost & Found REST API (FastAPI)

A production-ready backend REST API for a Lost & Found system, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

The API allows users to report lost and found items, list all items, view a single item, update item details, and delete items.

---

### Features

- **FastAPI** application with modular structure and routers
- **SQLAlchemy ORM** with `Item` model
- **SQLite** database for persistence
- **Pydantic** request/response schemas
- **Dependency-injected** database session
- Clean, production-readable code suitable for GitHub portfolio projects

---

### Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Uvicorn

---

### Project Structure

```text
lost-found-api/
│
├── app/
│   ├── main.py          # FastAPI application entrypoint
│   ├── database.py      # Database engine, session, Base
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Data-access / business logic
│   └── routers/
│       └── items.py     # Item-related API routes
│
├── requirements.txt
├── README.md
└── .gitignore