"""Shared test fixtures for the backend test suite."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import Base, get_db
from app.main import app

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///./data/storage/test_product_intelligence.db"


@pytest.fixture(scope="session", autouse=True)
def _setup_test_env():
    """Set environment variables for the test session."""
    os.environ["APP_ENV"] = "development"
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["LOG_LEVEL"] = "WARNING"


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine that persists across the session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()
    # Clean up the test database file
    db_path = TEST_DATABASE_URL.replace("sqlite:///", "")
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture()
def db_session(test_engine) -> Generator[Session, None, None]:
    """Provide a transactional database session that rolls back after each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(test_engine) -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with an isolated database session."""

    def override_get_db():
        connection = test_engine.connect()
        transaction = connection.begin()
        session = Session(bind=connection)
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
            connection.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def client_no_db_override() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client using the real database session."""
    with TestClient(app) as c:
        yield c
