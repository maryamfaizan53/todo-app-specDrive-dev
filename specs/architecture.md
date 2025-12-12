# Architecture Specification

## System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser (User)                        │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTPS
                             │
┌────────────────────────────▼────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                   http://localhost:3000                      │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Better    │  │     Pages    │  │  Components  │       │
│  │    Auth     │  │  (App Router)│  │  (Tailwind)  │       │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                │                  │                │
│         └────────────────┴──────────────────┘                │
│                          │                                   │
│                   ┌──────▼────────┐                          │
│                   │   API Client  │                          │
│                   │  (lib/api.js) │                          │
│                   └──────┬────────┘                          │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           │ Authorization: Bearer <JWT>
                           │ HTTP REST API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Backend (FastAPI)                         │
│                   http://localhost:8000                      │
│                                                               │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ JWT Verify    │  │  API Routes  │  │   SQLModel   │     │
│  │  Middleware   │  │ (user_id    │  │    Models    │     │
│  │ (auth.py)     │  │  validation) │  │              │     │
│  └───────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│          │                 │                  │              │
│          └─────────────────┴──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             │ SQL Queries (filtered by user_id)
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                   Database (Neon PostgreSQL)                  │
│                                                                │
│  ┌──────────────────┐      ┌──────────────────┐             │
│  │   users table    │      │   tasks table    │             │
│  │  - id (PK)       │      │  - id (PK)       │             │
│  │  - email         │      │  - user_id (FK)  │             │
│  │  - ...           │      │  - title         │             │
│  │                  │      │  - completed     │             │
│  └──────────────────┘      └──────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Frontend (Next.js)

**Better Auth Integration**:
- User sign-up and login
- JWT token issuing
- Session management
- Token storage (secure practices)

**API Client (`lib/api.js`)**:
- Attach JWT token to all requests: `Authorization: Bearer <token>`
- Handle API responses (200, 401, 403, 404, 422, 500)
- Redirect to login on 401
- Display error messages on failures

**Pages (App Router)**:
- `/app/page.js` - Home/landing page
- `/app/todos/page.js` - Main todo list with filters
- `/app/todos/new/page.js` - Create new task form
- `/app/todos/[id]/page.js` - Edit task form

**Components**:
- `Navbar` - Navigation with user info and logout
- `TodoList` - Display list of tasks
- `TodoItem` - Individual task with actions
- `TodoForm` - Create/edit task form
- `TodoFilters` - Filter, sort, and search controls

### Backend (FastAPI)

**Authentication (`app/auth.py`)**:
- JWT verification using `BETTER_AUTH_SECRET`
- Extract `user_id` from JWT payload
- Dependency injection for protected routes
- Return 401 for invalid/missing tokens

**API Routes (`app/api/tasks.py`)**:
- Validate path `user_id` matches JWT `user_id`
- Return 403 for user_id mismatch
- Filter all database queries by `user_id`
- Proper error handling and status codes

**Models (`app/models.py`)**:
- SQLModel classes for database tables
- Relationships between users and tasks

**Schemas (`app/schemas.py`)**:
- Pydantic models for request validation
- Response serialization

**Database (`app/db.py`)**:
- Database connection and session management
- Connection string from environment
- Auto-create tables on startup

### Database (Neon PostgreSQL)

**Users Table**:
- Managed by Better Auth
- Contains user credentials and profile

**Tasks Table**:
- `id`: Primary key (UUID or auto-increment)
- `user_id`: Foreign key to users table
- `title`: Task title (required)
- `description`: Task description (optional)
- `completed`: Boolean completion status
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Security Architecture

### Authentication Flow

1. User logs in via Better Auth frontend
2. Better Auth validates credentials
3. Better Auth issues JWT with payload:
   ```json
   {
     "sub": "<user_id>",
     "email": "<user_email>",
     "iat": <issued_at>,
     "exp": <expires_at>
   }
   ```
4. Frontend stores JWT securely
5. Frontend includes JWT in all API requests

### Authorization Flow

1. Frontend sends request with `Authorization: Bearer <JWT>`
2. Backend JWT middleware verifies signature using `BETTER_AUTH_SECRET`
3. Backend extracts `user_id` from token
4. Backend validates path `user_id` matches token `user_id`
5. Backend filters all queries by `user_id`
6. Return 401 if token invalid, 403 if user_id mismatch

### Data Isolation

Every database query MUST include `user_id` filter:

```python
# CORRECT - filtered by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == current_user["id"])
).all()

# WRONG - returns all users' tasks
tasks = session.exec(select(Task)).all()
```

## API Architecture

### RESTful Endpoints

All task endpoints follow pattern: `/api/{user_id}/tasks/*`

- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Request/Response Format

**Content-Type**: `application/json`

**Authentication**: `Authorization: Bearer <JWT>`

**Error Response Format**:
```json
{
  "detail": "Error message"
}
```

## Technology Decisions

### Why Next.js App Router?
- Modern React architecture with server components
- File-based routing simplifies navigation
- Built-in optimizations for production

### Why FastAPI?
- High performance async Python framework
- Automatic API documentation (OpenAPI/Swagger)
- Excellent Pydantic integration for validation
- Native async/await support

### Why SQLModel?
- Combines SQLAlchemy ORM with Pydantic validation
- Type hints for better IDE support
- Single model definition for DB and API schemas

### Why Neon PostgreSQL?
- Serverless Postgres with generous free tier
- Automatic scaling and branching
- Compatible with standard PostgreSQL tools

### Why Better Auth?
- Modern authentication for Next.js
- Built-in JWT support
- Easy integration with frontend

## Development Environment

### Local Development Setup

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Environment Variables**:
- Backend `.env`: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `CORS_ORIGINS`
- Frontend `.env.local`: `NEXT_PUBLIC_API_URL`, `BETTER_AUTH_SECRET`

### Testing Strategy

**Backend Tests** (pytest):
- Unit tests for business logic
- Integration tests for API endpoints
- Authorization tests for JWT validation
- Database tests for user_id isolation

**Frontend Tests** (manual):
- User flows (sign up, login, CRUD operations)
- Error handling (network failures, 401, 403)
- Responsive design on mobile and desktop

## Deployment Considerations

- Backend: Deploy to Heroku, Render, or Railway
- Frontend: Deploy to Vercel or Netlify
- Database: Use Neon PostgreSQL production instance
- Environment: Use separate `.env` for production with secure secrets
- CORS: Update `CORS_ORIGINS` to match production frontend URL
