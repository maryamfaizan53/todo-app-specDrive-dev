# Todo API Backend

FastAPI backend for the Todo Full-Stack Web Application with JWT authentication and user data isolation.

## Features

- **FastAPI**: Modern Python web framework
- **SQLModel**: ORM with Pydantic integration
- **JWT Authentication**: Secure token-based auth
- **User Data Isolation**: All queries filtered by user_id
- **Neon PostgreSQL**: Cloud database with SQLite fallback
- **Auto-generated API Docs**: OpenAPI/Swagger UI

## Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Configure environment variables in `.env`:
   ```
   DATABASE_URL=sqlite:///./todo.db  # or Neon PostgreSQL URL
   BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long
   CORS_ORIGINS=http://localhost:3000
   ```

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks` | List all tasks (with filters) |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### Query Parameters (GET /api/{user_id}/tasks)

- `completed`: Filter by completion status (true/false)
- `search`: Search in title and description
- `sort`: Sort by field (created_at, updated_at, title)
- `order`: Sort order (asc, desc)

## Testing

### Run Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_tasks.py
```

### Run with Coverage

```bash
pytest --cov=app tests/
```

## Database

### SQLite (Development)

By default, uses SQLite database stored in `todo.db` file.

### Neon PostgreSQL (Production)

Set `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

### Schema

The database uses the following schema:

**tasks** table:
- `id` (VARCHAR): Primary key (UUID)
- `user_id` (VARCHAR): Foreign key to users
- `title` (VARCHAR): Task title
- `description` (TEXT): Optional description
- `completed` (BOOLEAN): Completion status
- `created_at` (TIMESTAMP): Creation time
- `updated_at` (TIMESTAMP): Last update time

## Security

### JWT Authentication

- All task endpoints require valid JWT token
- Token must be signed with `BETTER_AUTH_SECRET`
- Token payload must contain user ID in `sub` claim
- Invalid/missing tokens return 401 Unauthorized

### User Data Isolation

- All queries filtered by `user_id` from JWT
- Path `user_id` must match JWT `user_id`
- Mismatched `user_id` returns 403 Forbidden
- Users cannot access other users' data

### Environment Variables

Never commit `.env` file to version control. Keep secrets secure:
- `BETTER_AUTH_SECRET`: Minimum 32 characters, random
- `DATABASE_URL`: Connection string with credentials

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── models.py        # SQLModel models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT verification
│   ├── db.py            # Database connection
│   └── api/
│       ├── __init__.py
│       └── tasks.py     # Task routes
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # pytest fixtures
│   └── test_tasks.py    # Task tests
├── .env.example         # Example environment variables
├── requirements.txt     # Python dependencies
└── README.md
```

## Development Guidelines

1. **Read specs first**: Always check `specs/` before coding
2. **Test-first**: Write tests before implementation
3. **User isolation**: Always filter by `user_id`
4. **JWT validation**: Use `get_current_user` dependency
5. **Error handling**: Use HTTPException with proper status codes
6. **Logging**: Log errors server-side, return generic messages to client

## Troubleshooting

### Database Connection Error

- Check `DATABASE_URL` in `.env`
- For SQLite, ensure write permissions in directory
- For Neon, verify connection string and network access

### JWT Verification Error

- Ensure `BETTER_AUTH_SECRET` matches frontend
- Check token format: `Bearer <token>`
- Verify token is not expired

### CORS Error

- Add frontend URL to `CORS_ORIGINS` in `.env`
- Restart server after changing `.env`

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Neon Documentation](https://neon.tech/docs/)
