# Database Schema Specification

## Overview

The Todo application uses **Neon PostgreSQL** as the primary database with **SQLite** as a fallback for local development. The schema is defined using **SQLModel**, which combines SQLAlchemy ORM with Pydantic validation.

## Database Configuration

### Connection Strings

**Neon PostgreSQL** (Production/Staging):
```
DATABASE_URL=postgresql://user:password@ep-example-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**SQLite** (Local Development):
```
DATABASE_URL=sqlite:///./todo.db
```

### Environment Variables

```bash
DATABASE_URL=<connection_string>
BETTER_AUTH_SECRET=<shared_secret>
```

---

## Tables

### 1. Users Table

**Note**: User table is managed by Better Auth. We reference it via foreign key but don't directly manage it.

**Schema** (Reference Only):
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 2. Tasks Table

**Purpose**: Store user tasks with completion status and timestamps

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False
    )
    title: str = Field(
        max_length=255,
        nullable=False
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000
    )
    completed: bool = Field(
        default=False,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

**SQL Definition**:
```sql
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID v4 as string |
| user_id | VARCHAR(255) | NOT NULL, FK, INDEXED | References users.id |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update timestamp (UTC) |

**Indexes**:
- Primary key on `id`
- Foreign key index on `user_id` (critical for user data isolation)
- Index on `created_at` for sorting
- Index on `completed` for filtering

**Constraints**:
- `title` cannot be empty
- `user_id` must reference existing user
- `completed` defaults to `false`
- Timestamps in UTC
- ON DELETE CASCADE: When user deleted, their tasks are deleted

---

## Pydantic Schemas

### TaskCreate (Request)

Used for creating new tasks.

```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
```

**Validation**:
- `title`: Required, 1-255 characters
- `description`: Optional, max 2000 characters

---

### TaskUpdate (Request)

Used for updating existing tasks.

```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
```

**Validation**:
- `title`: Required, 1-255 characters
- `description`: Optional, max 2000 characters

**Note**: Does NOT include `completed` field (use separate endpoint for toggling)

---

### TaskComplete (Request)

Used for toggling task completion.

```python
from pydantic import BaseModel

class TaskComplete(BaseModel):
    completed: bool
```

**Validation**:
- `completed`: Required boolean

---

### TaskResponse (Response)

Used for returning task data to client.

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from ORM model
```

**Fields**:
- All fields from Task model
- Timestamps serialized as ISO 8601 strings

---

## Database Operations

### Connection Management

**Database Session** (`backend/app/db.py`):
```python
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

def create_db_and_tables():
    """Create all tables on application startup"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session
```

**Usage in Routes**:
```python
from fastapi import Depends
from sqlmodel import Session
from app.db import get_session

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    session: Session = Depends(get_session)
):
    # Use session for queries
    pass
```

---

### CRUD Operations

**Create Task**:
```python
from app.models import Task
from app.schemas import TaskCreate

def create_task(user_id: str, task_data: TaskCreate, session: Session) -> Task:
    db_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

**List Tasks** (with user_id filter):
```python
from sqlmodel import select
from app.models import Task

def list_tasks(user_id: str, session: Session) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
```

**Get Single Task**:
```python
from sqlmodel import select
from app.models import Task

def get_task(user_id: str, task_id: str, session: Session) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    return task
```

**Update Task**:
```python
from app.models import Task
from app.schemas import TaskUpdate
from datetime import datetime

def update_task(task: Task, task_data: TaskUpdate, session: Session) -> Task:
    task.title = task_data.title
    task.description = task_data.description
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Delete Task**:
```python
from app.models import Task

def delete_task(task: Task, session: Session) -> None:
    session.delete(task)
    session.commit()
```

**Toggle Completion**:
```python
from app.models import Task
from datetime import datetime

def toggle_completion(task: Task, completed: bool, session: Session) -> Task:
    task.completed = completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

## Data Integrity Rules

### User Data Isolation

**CRITICAL**: Every query MUST filter by `user_id`:

```python
# CORRECT - filtered by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()

# WRONG - returns all users' tasks
tasks = session.exec(select(Task)).all()  # ❌ FORBIDDEN
```

### Foreign Key Constraints

- `ON DELETE CASCADE`: When user is deleted, all their tasks are deleted
- Prevents orphaned tasks
- Better Auth manages user lifecycle

### Timestamp Management

- Always use `datetime.utcnow()` for consistency
- Auto-set `created_at` on insert
- Auto-update `updated_at` on modifications
- Serialize as ISO 8601 in responses

### Validation

- Database-level: NOT NULL, length limits, foreign keys
- Application-level: Pydantic schemas validate before DB operations
- Frontend-level: Basic validation on forms

---

## Migrations

### Initial Setup

**For Development** (SQLite):
```python
# In app/main.py on startup
from app.db import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

**For Production** (Neon PostgreSQL):
Use Alembic for migrations (future enhancement).

### Schema Changes

**Phase II**: No migrations needed (fresh setup)

**Future Phases**: Use Alembic for schema versioning
```bash
alembic init alembic
alembic revision --autogenerate -m "Add column"
alembic upgrade head
```

---

## Testing

### Test Database

Use separate SQLite database for tests:

```python
# In tests/conftest.py
import pytest
from sqlmodel import create_engine, Session, SQLModel

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

### Test Data

Create test tasks with different user_ids:

```python
@pytest.fixture
def test_task(session):
    task = Task(
        user_id="test-user-123",
        title="Test Task",
        description="Test Description",
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Test Isolation

- Use in-memory SQLite for tests
- Each test gets fresh database
- No shared state between tests

---

## Performance Considerations

### Indexes

- `user_id`: Essential for filtering (most queries)
- `created_at`: Useful for sorting
- `completed`: Useful for filtering by status

### Query Optimization

- Always filter by `user_id` first (uses index)
- Limit result sets (add pagination in future)
- Use select specific columns if needed (not entire rows)

### Connection Pooling

- SQLModel/SQLAlchemy handles pooling
- Configure pool size for production:
  ```python
  engine = create_engine(
      DATABASE_URL,
      pool_size=10,
      max_overflow=20
  )
  ```

---

## Security

### SQL Injection Prevention

- Use SQLModel/SQLAlchemy ORM (parameterized queries)
- Never concatenate user input into queries
- Validate all input with Pydantic

### Data Access Control

- Always filter by `user_id` from JWT
- Validate `user_id` in path matches JWT
- Use foreign key constraints

### Secrets Management

- Database credentials in `.env` only
- Never commit `.env` to version control
- Use different credentials for dev/prod

---

## Backup and Recovery

### Development

- SQLite file: `todo.db`
- Copy file for backup
- No automated backups needed

### Production (Neon)

- Neon provides automatic backups
- Point-in-time recovery available
- Export data via pg_dump if needed

---

## Future Enhancements

Phase III and beyond may include:

- Task categories/tags (new table)
- Task priorities (new column)
- Due dates (new column)
- Task sharing (junction table)
- Soft delete (deleted_at column)
- Full-text search (PostgreSQL FTS)
- Audit log (separate table)
- Pagination (LIMIT/OFFSET)

These are OUT OF SCOPE for Phase II.
