from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import Base, engine
from .routers import items


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    app = FastAPI(
        title="Lost & Found API",
        version="1.0.0",
        description=(
            "A production-ready REST API for managing lost and found items. "
            "Built with FastAPI, SQLAlchemy, and SQLite."
        ),
    )

    # Configure CORS (adjust allowed origins as needed for production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to trusted domains.
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(items.router)

    @app.get(
        "/",
        tags=["health"],
        summary="Health check",
    )
    def health_check() -> dict[str, str]:
        """
        Simple health check endpoint to verify that the service is running.
        """
        return {"status": "ok"}

    return app


# Create all database tables on startup if they do not exist.
Base.metadata.create_all(bind=engine)

app = create_application()