"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional)")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str = Field(..., min_length=1, max_length=255, description="Updated task title")
    description: Optional[str] = Field(None, max_length=2000, description="Updated task description (optional)")


class TaskComplete(BaseModel):
    """Schema for toggling task completion."""
    completed: bool = Field(..., description="Completion status")


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from ORM model
