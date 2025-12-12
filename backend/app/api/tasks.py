"""
Task API routes with JWT authentication and user data isolation.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskComplete, TaskResponse
from app.auth import get_current_user
from app.db import get_session

router = APIRouter()


@router.post("/api/{user_id}/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from path (must match authenticated user)
        task: Task creation data
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TaskResponse: Created task

    Raises:
        403: If user_id doesn't match authenticated user
        422: If validation fails
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot create tasks for other users"
        )

    # Create new task
    db_task = Task(
        user_id=user_id,
        title=task.title,
        description=task.description
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/api/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort: str = Query("created_at", description="Sort by field (created_at, updated_at, title)"),
    order: str = Query("desc", description="Sort order (asc, desc)")
):
    """
    List all tasks for the authenticated user with optional filters.

    Args:
        user_id: User ID from path (must match authenticated user)
        current_user: Authenticated user from JWT
        session: Database session
        completed: Optional filter by completion status
        search: Optional search query for title/description
        sort: Field to sort by
        order: Sort order (asc or desc)

    Returns:
        List[TaskResponse]: List of tasks

    Raises:
        403: If user_id doesn't match authenticated user
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot access other users' tasks"
        )

    # Build query with user_id filter
    statement = select(Task).where(Task.user_id == user_id)

    # Apply completed filter if provided
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Apply search filter if provided (case-insensitive)
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where(
            (Task.title.ilike(search_pattern)) |
            (Task.description.ilike(search_pattern))
        )

    # Apply sorting
    sort_field = getattr(Task, sort, Task.created_at)
    if order == "asc":
        statement = statement.order_by(sort_field.asc())
    else:
        statement = statement.order_by(sort_field.desc())

    tasks = session.exec(statement).all()
    return tasks


@router.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TaskResponse: Task details

    Raises:
        403: If user_id doesn't match authenticated user
        404: If task not found or belongs to different user
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot access other users' tasks"
        )

    # Query task with user_id filter
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        task_update: Updated task data
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        403: If user_id doesn't match authenticated user
        404: If task not found
        422: If validation fails
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot update other users' tasks"
        )

    # Query task with user_id filter
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Update task fields
    task.title = task_update.title
    task.description = task_update.description
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/api/{user_id}/tasks/{task_id}", status_code=204)
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        403: If user_id doesn't match authenticated user
        404: If task not found
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot delete other users' tasks"
        )

    # Query task with user_id filter
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return None


@router.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    completion: TaskComplete,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.

    Args:
        user_id: User ID from path (must match authenticated user)
        task_id: Task ID
        completion: Completion status
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        TaskResponse: Updated task

    Raises:
        403: If user_id doesn't match authenticated user
        404: If task not found
    """
    # Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Cannot modify other users' tasks"
        )

    # Query task with user_id filter
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Update completion status
    task.completed = completion.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
