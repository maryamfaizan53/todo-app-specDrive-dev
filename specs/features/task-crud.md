# Feature: Task CRUD Operations

## Overview

Implement complete Create, Read, Update, Delete (CRUD) operations for tasks with proper JWT authentication and user data isolation.

## User Stories

### US-1: Create Task (Priority: P1)

**As a** logged-in user
**I want to** create a new task
**So that** I can track things I need to do

**Acceptance Criteria**:
- User can submit a form with task title and optional description
- Task is created with `completed: false` by default
- Task is associated with authenticated user's `user_id`
- Created task appears immediately in user's task list
- Frontend redirects to task list after successful creation
- Backend returns 422 if title is empty
- Backend returns 401 if JWT is missing or invalid

**API Endpoint**: `POST /api/{user_id}/tasks`

**Test Scenarios**:
1. Create task with valid title and description
2. Create task with only title (no description)
3. Attempt to create task without title (should fail with 422)
4. Attempt to create task without JWT (should fail with 401)
5. Attempt to create task with mismatched user_id (should fail with 403)

---

### US-2: List Tasks (Priority: P1)

**As a** logged-in user
**I want to** see all my tasks
**So that** I can review what I need to do

**Acceptance Criteria**:
- User sees all their tasks on the main page
- Tasks include title, description, completion status, and timestamps
- Tasks are sorted by created_at (newest first) by default
- User cannot see tasks belonging to other users
- Empty list shows friendly message
- Backend returns 401 if JWT is missing or invalid

**API Endpoint**: `GET /api/{user_id}/tasks`

**Query Parameters** (optional):
- `completed`: Filter by completion status (true/false)
- `search`: Search in title and description
- `sort`: Sort by field (created_at, updated_at, title)

**Test Scenarios**:
1. List tasks for user with multiple tasks
2. List tasks for user with no tasks (empty array)
3. List tasks with completed filter
4. List tasks with search query
5. Attempt to list tasks without JWT (should fail with 401)
6. Attempt to list tasks with mismatched user_id (should fail with 403)

---

### US-3: View Single Task (Priority: P2)

**As a** logged-in user
**I want to** view details of a specific task
**So that** I can see all information about it

**Acceptance Criteria**:
- User can view full details of their task
- Task includes all fields: id, title, description, completed, created_at, updated_at
- Backend returns 404 if task doesn't exist
- Backend returns 403 if task belongs to different user
- Backend returns 401 if JWT is missing or invalid

**API Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Test Scenarios**:
1. View existing task owned by user
2. Attempt to view non-existent task (should fail with 404)
3. Attempt to view task owned by different user (should fail with 403)
4. Attempt to view task without JWT (should fail with 401)

---

### US-4: Update Task (Priority: P1)

**As a** logged-in user
**I want to** edit my task
**So that** I can correct or update the information

**Acceptance Criteria**:
- User can update task title and/or description
- `updated_at` timestamp is automatically updated
- `completed` status is NOT changed by this endpoint (use complete endpoint)
- Backend returns 404 if task doesn't exist
- Backend returns 403 if task belongs to different user
- Backend returns 401 if JWT is missing or invalid
- Backend returns 422 if updated title is empty

**API Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Test Scenarios**:
1. Update task title and description
2. Update only task title
3. Update only task description
4. Attempt to update with empty title (should fail with 422)
5. Attempt to update non-existent task (should fail with 404)
6. Attempt to update task owned by different user (should fail with 403)
7. Attempt to update task without JWT (should fail with 401)

---

### US-5: Delete Task (Priority: P1)

**As a** logged-in user
**I want to** delete a task
**So that** I can remove tasks I no longer need

**Acceptance Criteria**:
- User can delete their task permanently
- Deleted task is removed from database
- Backend returns 404 if task doesn't exist
- Backend returns 403 if task belongs to different user
- Backend returns 401 if JWT is missing or invalid
- Frontend confirms deletion before sending request

**API Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Test Scenarios**:
1. Delete existing task owned by user
2. Attempt to delete non-existent task (should fail with 404)
3. Attempt to delete task owned by different user (should fail with 403)
4. Attempt to delete task without JWT (should fail with 401)
5. Verify task is removed from database after deletion

---

### US-6: Toggle Task Completion (Priority: P1)

**As a** logged-in user
**I want to** mark a task as complete or incomplete
**So that** I can track my progress

**Acceptance Criteria**:
- User can toggle task completion with single click
- Completed tasks show visual indicator (e.g., strikethrough, checkmark)
- `updated_at` timestamp is automatically updated
- Backend returns 404 if task doesn't exist
- Backend returns 403 if task belongs to different user
- Backend returns 401 if JWT is missing or invalid

**API Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Request Body**: `{ "completed": true/false }`

**Test Scenarios**:
1. Mark incomplete task as complete
2. Mark complete task as incomplete
3. Attempt to toggle completion of non-existent task (should fail with 404)
4. Attempt to toggle completion of task owned by different user (should fail with 403)
5. Attempt to toggle completion without JWT (should fail with 401)

---

## Technical Requirements

### Backend Implementation

**Dependencies**:
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.auth import get_current_user
from app.db import get_session
```

**Route Pattern**:
```python
@router.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # Implementation...
```

**User ID Validation**: Every endpoint must validate that `user_id` from path matches `current_user["id"]` from JWT.

**Database Filtering**: Every query must filter by `user_id`:
```python
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()
```

### Frontend Implementation

**API Client Usage**:
```javascript
// Create task
await apiRequest(`/api/${userId}/tasks`, {
  method: 'POST',
  body: JSON.stringify({ title, description })
});

// List tasks
const tasks = await apiRequest(`/api/${userId}/tasks`);

// Update task
await apiRequest(`/api/${userId}/tasks/${taskId}`, {
  method: 'PUT',
  body: JSON.stringify({ title, description })
});

// Delete task
await apiRequest(`/api/${userId}/tasks/${taskId}`, {
  method: 'DELETE'
});

// Toggle completion
await apiRequest(`/api/${userId}/tasks/${taskId}/complete`, {
  method: 'PATCH',
  body: JSON.stringify({ completed })
});
```

**Error Handling**:
- 401: Redirect to login
- 403: Show error message
- 404: Show "Task not found" message
- 422: Show validation errors
- 500: Show generic error message

## Testing Requirements

### Backend Tests (pytest)

File: `backend/tests/test_tasks.py`

**Test Categories**:
1. **Happy Path**: All operations with valid data
2. **Authorization**: All operations with invalid/missing JWT
3. **Ownership**: All operations with mismatched user_id
4. **Validation**: Create/update with invalid data
5. **Not Found**: Operations on non-existent tasks

**Test Fixtures**:
```python
@pytest.fixture
def mock_user():
    return {"id": "user-123", "email": "test@example.com"}

@pytest.fixture
def mock_token():
    # Generate valid JWT for testing
    pass
```

### Frontend Tests (Manual)

**Test Checklist**:
- [ ] Create task with valid data
- [ ] Create task with empty title shows error
- [ ] List tasks shows all user's tasks
- [ ] Update task saves changes
- [ ] Delete task removes from list
- [ ] Toggle completion updates UI
- [ ] Logout and login as different user shows different tasks
- [ ] All operations show loading state
- [ ] All errors show user-friendly messages

## Success Criteria

Feature is complete when:
- [ ] All 6 user stories are implemented
- [ ] All API endpoints match specification
- [ ] All backend tests pass
- [ ] All manual frontend tests pass
- [ ] User data isolation is verified
- [ ] JWT authentication is enforced on all endpoints
- [ ] Code follows constitution principles
