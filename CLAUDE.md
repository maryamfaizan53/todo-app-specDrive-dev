# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Phase II: Todo Full-Stack Web Application** — a complete full-stack implementation using:
- **Backend**: FastAPI + SQLModel + Neon Postgres + JWT authentication
- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + JavaScript + Better Auth

The project follows **Spec-Driven Development (SDD)** with strict adherence to the constitution at `.specify/memory/constitution.md`.

## Critical Architecture Principles

### 1. Spec-First, Always
**NEVER write code without first reading the relevant specs**:
- `specs/overview.md` - Project goals and context
- `specs/architecture.md` - System architecture
- `specs/features/*.md` - Feature requirements
- `specs/api/rest-endpoints.md` - API contracts (NON-NEGOTIABLE)
- `specs/database/schema.md` - Data models
- `specs/ui/*.md` - UI specifications

### 2. Security is Non-Negotiable
**ALL API endpoints enforce JWT authentication**:
- Better Auth on frontend issues JWT tokens
- FastAPI backend verifies JWT on EVERY protected endpoint
- Path `user_id` MUST match JWT token `user_id` claim
- Cross-user data access is FORBIDDEN (enforced at DB query level)
- Return 401 for missing/invalid tokens, 403 for user_id mismatch

### 3. User Data Isolation
**Every database query MUST filter by `user_id`**:
```python
# Backend pattern - ALWAYS filter by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == current_user["id"])
).all()
```

### 4. Test-First Development (Red-Green-Refactor)
1. Write tests that FAIL first (Red)
2. Implement minimum code to pass (Green)
3. Refactor while keeping tests green
Required: contract tests, integration tests, auth tests

## Development Workflow Commands

### Primary Workflow (Spec → Plan → Tasks → Implement)

1. **Create/Update Feature Specification**
   ```bash
   /sp.specify <feature description>
   ```
   - Generates branch name and creates `specs/<###-feature>/spec.md`
   - Extracts user stories with priorities (P1, P2, P3)

2. **Generate Implementation Plan**
   ```bash
   /sp.plan
   ```
   - Creates `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
   - Validates against constitution
   - Resolves technical unknowns through research

3. **Generate Actionable Tasks**
   ```bash
   /sp.tasks
   ```
   - Creates `tasks.md` organized by user story priority
   - Each story is independently testable
   - Identifies parallel execution opportunities

4. **Execute Implementation**
   ```bash
   /sp.implement
   ```
   - Processes tasks from `tasks.md`
   - Enforces test-first (Red-Green-Refactor)
   - Auto-commits after each task completion

### Supporting Commands

- **Record Architectural Decisions**: `/sp.adr <decision-title>`
- **Analyze Spec Consistency**: `/sp.analyze`
- **Create Feature Checklist**: `/sp.checklist`
- **Clarify Spec Ambiguities**: `/sp.clarify`
- **Commit & Create PR**: `/sp.git.commit_pr`

### Utility Scripts

```bash
# Create new feature with auto-numbering
.specify/scripts/bash/create-new-feature.sh --json "<description>" --number N --short-name "feature-name"

# Create PHR (Prompt History Record) after any significant work
.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json

# Create ADR for architectural decisions
.specify/scripts/bash/create-adr.sh "<decision-title>"
```

## Repository Structure

```
to-do-web/
├── .specify/
│   ├── memory/constitution.md          # Project principles (VERSION 1.0.0)
│   ├── templates/                      # Templates for spec, plan, tasks, ADR, PHR
│   └── scripts/bash/                   # Automation scripts
├── .claude/
│   ├── agents/                         # Specialized agents (8 total)
│   ├── commands/                       # Slash commands (sp.* workflows)
│   └── skills/                         # Reusable skills (8 total)
├── specs/<###-feature>/
│   ├── spec.md                         # User stories, requirements, success criteria
│   ├── plan.md                         # Technical design, architecture
│   ├── tasks.md                        # Actionable task breakdown
│   ├── research.md                     # Technology decisions
│   ├── data-model.md                   # Entity models
│   ├── quickstart.md                   # Manual test scenarios
│   └── contracts/                      # API endpoint contracts
├── history/
│   ├── prompts/                        # PHRs organized by stage/feature
│   └── adr/                            # Architecture Decision Records
├── backend/                            # FastAPI application (TO BE CREATED)
│   ├── app/
│   │   ├── main.py                     # FastAPI app with CORS for localhost:3000
│   │   ├── models/                     # SQLModel database models
│   │   ├── routers/                    # API route handlers
│   │   ├── auth.py                     # JWT verification middleware
│   │   └── db.py                       # Database session management
│   ├── tests/
│   │   ├── test_tasks.py               # Task CRUD + auth tests
│   │   └── conftest.py                 # pytest fixtures
│   └── requirements.txt                # Python dependencies
└── frontend/                           # Next.js application (TO BE CREATED)
    ├── app/
    │   ├── layout.js                   # Root layout
    │   ├── page.js                     # Home page
    │   └── todos/                      # Todo pages
    ├── components/
    │   ├── Navbar.js
    │   ├── TodoList.js
    │   ├── TodoItem.js
    │   ├── TodoForm.js
    │   └── TodoFilters.js
    ├── lib/
    │   └── api.js                      # API client with JWT attachment
    └── package.json                    # Node dependencies
```

## Backend Architecture (FastAPI + SQLModel)

### Running the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Testing the Backend
```bash
cd backend
pytest                                   # Run all tests
pytest tests/test_tasks.py              # Run specific test file
pytest -v -k "test_create_task"         # Run specific test
```

### Key Backend Patterns

**JWT Verification Dependency**:
```python
# backend/app/auth.py
from fastapi import Depends, HTTPException, Header
import jwt
import os

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        return payload  # Contains user_id
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Route with User Ownership Validation**:
```python
# backend/app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user

router = APIRouter()

@router.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate user_id from path matches authenticated user
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Filter all queries by user_id
    db_task = Task(user_id=user_id, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

## Frontend Architecture (Next.js + Better Auth)

### Running the Frontend
```bash
cd frontend
npm install
npm run dev                              # Runs on http://localhost:3000
```

### Testing the Frontend
```bash
cd frontend
npm test                                 # Run tests (if configured)
npm run build                            # Validate build
```

### Key Frontend Patterns

**API Client with JWT**:
```javascript
// frontend/lib/api.js
export async function apiRequest(endpoint, options = {}) {
  const token = getTokenFromAuth();  // Better Auth session

  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (response.status === 401) {
    // Token expired, redirect to login
    window.location.href = '/login';
    return;
  }

  if (response.status === 403) {
    throw new Error('Forbidden: Access denied');
  }

  return response.json();
}
```

## Specialized Agents (Auto-invoked)

The repository includes 8 specialized agents that handle specific tasks:

1. **implementation-planner** - Creates multi-phase implementation plans
2. **research-specialist** - Finds libraries, best practices, documentation
3. **db-designer** - Creates SQLModel models and migrations
4. **api-designer** - Defines REST routes and schemas
5. **backend-impl** - Implements FastAPI endpoints with tests
6. **frontend-impl** - Implements Next.js pages and components
7. **auth-integration-specialist** - Sets up Better Auth + JWT verification
8. **test-and-qa** - Generates test plans and coverage

These agents are automatically invoked when relevant tasks are detected.

## Environment Configuration

### Backend `.env`
```bash
DATABASE_URL=postgresql://user:password@host/dbname  # Neon connection string
BETTER_AUTH_SECRET=<shared-secret-with-frontend>
CORS_ORIGINS=http://localhost:3000
```

### Frontend `.env.local`
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<shared-secret-with-backend>
```

**CRITICAL**: Never commit `.env` files. Use `.env.example` for documentation.

## Constitution Compliance

Every change MUST comply with the 8 core principles in `.specify/memory/constitution.md`:

1. ✅ Spec-Driven Development - Read specs before coding
2. ✅ JWT Authentication & Authorization - Enforce on all endpoints
3. ✅ User Data Isolation - Filter all queries by user_id
4. ✅ Test-First Development - Write tests before implementation
5. ✅ API Contract Validation - Match specs/api/rest-endpoints.md exactly
6. ✅ Frontend-Backend Integration - Proper error handling
7. ✅ Database Migrations Safety - Reversible with rollback SQL
8. ✅ Observability & Error Handling - Structured logging, proper status codes

## Prompt History Records (PHRs)

After completing any significant work, create a PHR:
```bash
.specify/scripts/bash/create-phr.sh --title "Brief description" --stage <stage> --json
```

**Stages**: `constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general`

**Routing**:
- Constitution work → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General work → `history/prompts/general/`

## Code Quality Standards

### Python (Backend)
- Use type hints for all function signatures
- Async/await for all database operations
- Pydantic models for request/response validation
- HTTPException for error responses (never bare exceptions)
- Session management via dependency injection

### JavaScript (Frontend)
- Functional components with hooks
- Error boundaries for error handling
- Loading states for async operations
- Consistent prop naming
- Tailwind utility classes (avoid custom CSS)

## Common Pitfalls to Avoid

1. ❌ **Writing code before reading specs** - Always read specs first
2. ❌ **Skipping user_id validation** - Every endpoint must validate ownership
3. ❌ **Hardcoding secrets** - Use environment variables
4. ❌ **Breaking API contracts** - Update spec FIRST, then code
5. ❌ **Implementing without tests** - Write failing tests first
6. ❌ **Cross-user data leaks** - Filter ALL queries by user_id
7. ❌ **Exposing internal errors** - Log details, return generic messages
8. ❌ **Forgetting CORS** - Backend must allow `http://localhost:3000`

## Workflow Summary

```
User Request
     ↓
/sp.specify → Create spec.md with user stories
     ↓
/sp.plan → Generate plan.md, research.md, contracts/
     ↓
/sp.tasks → Generate tasks.md (organized by user story)
     ↓
/sp.implement → Execute tasks (test-first)
     ↓
Create PHR → Document work in history/prompts/
     ↓
/sp.git.commit_pr → Commit and create PR
```

For architectural decisions during planning, suggest ADR creation with `/sp.adr <title>`.
