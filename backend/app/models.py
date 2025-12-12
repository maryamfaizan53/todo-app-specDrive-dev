"""
Database models using SQLModel.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Foreign key to users table (managed by Better Auth)
        title: Task title (required, max 255 chars)
        description: Task description (optional, max 2000 chars)
        completed: Completion status (default: False)
        created_at: Creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
    """
    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    user_id: str = Field(
        index=True,
        nullable=False,
        description="References users.id from Better Auth"
    )
    title: str = Field(
        max_length=255,
        nullable=False,
        description="Task title"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional)"
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp (UTC)"
    )
