# REST API Endpoints Specification

## Base URL

**Development**: `http://localhost:8000`
**Production**: TBD

## Authentication

All endpoints require JWT authentication via `Authorization` header:

```
Authorization: Bearer <JWT_TOKEN>
```

## Common Response Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Missing or invalid JWT |
| 403 | Forbidden | user_id mismatch |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

## Error Response Format

```json
{
  "detail": "Error message description"
}
```

---

## Endpoints

### 1. Create Task

**Endpoint**: `POST /api/{user_id}/tasks`

**Description**: Create a new task for the authenticated user

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id

**Request Headers**:
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Request Schema**:
- `title` (string, required): Task title, max 255 characters
- `description` (string, optional): Task description, max 2000 characters

**Success Response** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-12T10:30:00Z",
  "updated_at": "2025-12-12T10:30:00Z"
}
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: user_id in path doesn't match JWT user_id
- 422: Title is empty or exceeds max length

**Example**:
```bash
curl -X POST http://localhost:8000/api/user-123/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

---

### 2. List Tasks

**Endpoint**: `GET /api/{user_id}/tasks`

**Description**: Get all tasks for the authenticated user with optional filters

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id

**Query Parameters** (all optional):
- `completed` (boolean): Filter by completion status (true/false)
- `search` (string): Search in title and description (case-insensitive)
- `sort` (string): Sort by field (created_at, updated_at, title), default: created_at
- `order` (string): Sort order (asc, desc), default: desc

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response** (200 OK):
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "user-123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-12T10:30:00Z",
    "updated_at": "2025-12-12T10:30:00Z"
  },
  {
    "id": "223e4567-e89b-12d3-a456-426614174001",
    "user_id": "user-123",
    "title": "Walk the dog",
    "description": null,
    "completed": true,
    "created_at": "2025-12-11T15:20:00Z",
    "updated_at": "2025-12-12T08:15:00Z"
  }
]
```

**Empty Result** (200 OK):
```json
[]
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: user_id in path doesn't match JWT user_id

**Examples**:

Get all tasks:
```bash
curl http://localhost:8000/api/user-123/tasks \
  -H "Authorization: Bearer eyJ..."
```

Filter completed tasks:
```bash
curl "http://localhost:8000/api/user-123/tasks?completed=true" \
  -H "Authorization: Bearer eyJ..."
```

Search tasks:
```bash
curl "http://localhost:8000/api/user-123/tasks?search=groceries" \
  -H "Authorization: Bearer eyJ..."
```

Sort by title:
```bash
curl "http://localhost:8000/api/user-123/tasks?sort=title&order=asc" \
  -H "Authorization: Bearer eyJ..."
```

---

### 3. Get Single Task

**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Description**: Get details of a specific task

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id
- `id` (string, required): Task ID (UUID)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-12T10:30:00Z",
  "updated_at": "2025-12-12T10:30:00Z"
}
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: Task belongs to different user
- 404: Task not found

**Example**:
```bash
curl http://localhost:8000/api/user-123/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer eyJ..."
```

---

### 4. Update Task

**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Description**: Update task title and/or description (not completion status)

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id
- `id` (string, required): Task ID (UUID)

**Request Headers**:
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables"
}
```

**Request Schema**:
- `title` (string, required): Updated task title, max 255 characters
- `description` (string, optional): Updated task description, max 2000 characters

**Success Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-123",
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken, vegetables",
  "completed": false,
  "created_at": "2025-12-12T10:30:00Z",
  "updated_at": "2025-12-12T11:45:00Z"
}
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: Task belongs to different user
- 404: Task not found
- 422: Title is empty or exceeds max length

**Example**:
```bash
curl -X PUT http://localhost:8000/api/user-123/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"title": "Buy groceries and cook dinner", "description": "Milk, eggs, bread, chicken, vegetables"}'
```

---

### 5. Delete Task

**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Description**: Permanently delete a task

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id
- `id` (string, required): Task ID (UUID)

**Request Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Success Response** (204 No Content):
```
(Empty response body)
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: Task belongs to different user
- 404: Task not found

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/user-123/tasks/123e4567-e89b-12d3-a456-426614174000 \
  -H "Authorization: Bearer eyJ..."
```

---

### 6. Toggle Task Completion

**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Description**: Toggle task completion status

**Path Parameters**:
- `user_id` (string, required): Must match JWT user_id
- `id` (string, required): Task ID (UUID)

**Request Headers**:
```
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "completed": true
}
```

**Request Schema**:
- `completed` (boolean, required): New completion status

**Success Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-12T10:30:00Z",
  "updated_at": "2025-12-12T12:00:00Z"
}
```

**Error Responses**:
- 401: Missing or invalid JWT
- 403: Task belongs to different user
- 404: Task not found
- 422: Invalid completion value

**Example**:
```bash
curl -X PATCH http://localhost:8000/api/user-123/tasks/123e4567-e89b-12d3-a456-426614174000/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{"completed": true}'
```

---

## Data Models

### Task Response Model

```json
{
  "id": "string (UUID)",
  "user_id": "string",
  "title": "string (max 255)",
  "description": "string | null (max 2000)",
  "completed": "boolean",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

### Task Create Model

```json
{
  "title": "string (required, max 255)",
  "description": "string | null (optional, max 2000)"
}
```

### Task Update Model

```json
{
  "title": "string (required, max 255)",
  "description": "string | null (optional, max 2000)"
}
```

### Task Complete Model

```json
{
  "completed": "boolean (required)"
}
```

---

## CORS Configuration

**Allowed Origins** (Development):
- `http://localhost:3000`

**Allowed Methods**:
- GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers**:
- Content-Type, Authorization

**Credentials**: Allowed

---

## Implementation Notes

### User ID Validation

Every endpoint MUST validate that `user_id` from path matches `user_id` from JWT:

```python
if current_user["id"] != user_id:
    raise HTTPException(status_code=403, detail="Forbidden")
```

### Database Filtering

Every query MUST filter by `user_id`:

```python
tasks = session.exec(
    select(Task).where(Task.user_id == user_id)
).all()
```

### Timestamp Handling

- Use UTC for all timestamps
- ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Auto-update `updated_at` on modifications

### Error Handling

- Log detailed errors server-side
- Return generic messages to client
- Never expose stack traces or internal details

### Testing

Test each endpoint with:
- Valid request
- Missing JWT
- Invalid JWT
- Mismatched user_id
- Invalid data
- Non-existent resource

---

## Versioning

**Current Version**: v1 (implicit)

**Breaking Changes**: Will require version increment in URL path (e.g., `/api/v2/...`)

---

## Rate Limiting

**Phase II**: No rate limiting (development only)

**Future**: Consider rate limiting for production:
- 100 requests per minute per user
- 1000 requests per hour per user
