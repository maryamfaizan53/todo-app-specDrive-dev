"""
Database connection and session management.
"""
from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create engine with appropriate settings
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    connect_args=connect_args
)


def create_db_and_tables():
    """
    Create all database tables on application startup.
    This is a simple approach for development. In production,
    use migrations (e.g., Alembic) for schema changes.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency for getting database session in route handlers.

    Usage:
        @router.get("/tasks")
        async def list_tasks(session: Session = Depends(get_session)):
            # Use session here
            pass

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
