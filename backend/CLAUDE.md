# Backend Development Guide

## Overview

This backend implements the Todo API using FastAPI with JWT authentication, SQLModel ORM, and Neon PostgreSQL.

## Key Principles

1. **JWT Authentication**: ALL endpoints require valid JWT except `/` and `/health`
2. **User Data Isolation**: ALWAYS filter queries by `user_id` from JWT
3. **User ID Validation**: ALWAYS validate path `user_id` matches JWT `user_id`
4. **Error Handling**: Return proper HTTP status codes, log details server-side
5. **Test-First**: Write tests before implementing features

## Code Patterns

### Route Handler Pattern

```python
@router.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # 1. Validate user_id matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2. Perform operation with user_id filter
    db_task = Task(user_id=user_id, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # 3. Return result
    return db_task
```

### Database Query Pattern

```python
# CORRECT - Always filter by user_id
statement = select(Task).where(Task.user_id == user_id)
tasks = session.exec(statement).all()

# WRONG - Never query without user_id filter
tasks = session.exec(select(Task)).all()  # ❌ FORBIDDEN
```

## Development Workflow

1. Read relevant specs in `/specs`
2. Write tests in `/backend/tests`
3. Run tests (they should fail - Red phase)
4. Implement feature in `/backend/app`
5. Run tests again (they should pass - Green phase)
6. Refactor if needed (keep tests green)

## Running Tests

```bash
cd backend
pytest                          # Run all tests
pytest tests/test_tasks.py      # Run specific file
pytest -v -k "test_create"      # Run specific test
pytest --cov=app                # Run with coverage
```

## Common Issues

### Database Connection
- Check `DATABASE_URL` in `.env`
- For SQLite: Ensure write permissions
- For Neon: Verify connection string

### JWT Errors
- Ensure `BETTER_AUTH_SECRET` matches frontend
- Check token format: `Bearer <token>`
- Verify token not expired

### CORS Errors
- Add frontend URL to `CORS_ORIGINS`
- Restart server after `.env` changes

## Security Checklist

- [ ] All endpoints use `get_current_user` dependency
- [ ] All routes validate `user_id` matches JWT
- [ ] All queries filter by `user_id`
- [ ] No secrets in code
- [ ] Error messages don't expose internals
- [ ] Input validation with Pydantic

## Reference

- Architecture: `/specs/architecture.md`
- API Contracts: `/specs/api/rest-endpoints.md`
- Database Schema: `/specs/database/schema.md`
- Constitution: `/.specify/memory/constitution.md`
