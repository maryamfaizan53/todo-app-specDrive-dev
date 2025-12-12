"""
Pytest configuration and fixtures for testing.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import jwt
import os

from app.main import app
from app.db import get_session
from app.models import Task


# Create in-memory SQLite database for tests
@pytest.fixture(name="session")
def session_fixture():
    """
    Create a fresh database session for each test.
    Uses in-memory SQLite for fast, isolated tests.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a TestClient with overridden database session.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user():
    """
    Test user data for JWT token generation.
    """
    return {
        "id": "test-user-123",
        "sub": "test-user-123",
        "email": "test@example.com"
    }


@pytest.fixture
def test_user_2():
    """
    Second test user for testing user isolation.
    """
    return {
        "id": "test-user-456",
        "sub": "test-user-456",
        "email": "test2@example.com"
    }


@pytest.fixture
def auth_token(test_user):
    """
    Generate valid JWT token for test user.
    """
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-minimum-32-characters-long")
    token = jwt.encode(test_user, secret, algorithm="HS256")
    return token


@pytest.fixture
def auth_token_user_2(test_user_2):
    """
    Generate valid JWT token for second test user.
    """
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-minimum-32-characters-long")
    token = jwt.encode(test_user_2, secret, algorithm="HS256")
    return token


@pytest.fixture
def auth_headers(auth_token):
    """
    Generate authorization headers with JWT token.
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def auth_headers_user_2(auth_token_user_2):
    """
    Generate authorization headers for second test user.
    """
    return {"Authorization": f"Bearer {auth_token_user_2}"}


@pytest.fixture
def sample_task(session: Session, test_user):
    """
    Create a sample task in the database for testing.
    """
    task = Task(
        user_id=test_user["id"],
        title="Sample Task",
        description="This is a sample task",
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture
def sample_tasks(session: Session, test_user):
    """
    Create multiple sample tasks for testing list operations.
    """
    tasks = [
        Task(
            user_id=test_user["id"],
            title="Task 1",
            description="First task",
            completed=False
        ),
        Task(
            user_id=test_user["id"],
            title="Task 2",
            description="Second task",
            completed=True
        ),
        Task(
            user_id=test_user["id"],
            title="Task 3",
            description="Third task",
            completed=False
        ),
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks
