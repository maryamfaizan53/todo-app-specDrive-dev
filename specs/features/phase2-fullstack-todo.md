# Phase II: Full-Stack Todo Application - Master Feature Spec

## Executive Summary

Complete implementation of a production-ready Todo Web Application with:
- **Frontend**: Next.js 14+ App Router, JavaScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI, SQLModel, Neon PostgreSQL, JWT authentication
- **Features**: Full CRUD operations, authentication, data isolation, filters, search

## Implementation Scope

### Phase II Deliverables

1. **Backend API** (`/backend`)
   - FastAPI application with SQLModel ORM
   - JWT authentication middleware
   - RESTful task endpoints with user_id validation
   - Comprehensive test suite with pytest
   - Neon PostgreSQL integration with SQLite fallback

2. **Frontend Application** (`/frontend`)
   - Next.js App Router application
   - Better Auth integration with JWT
   - Task management UI (create, list, edit, delete, complete)
   - Responsive design with Tailwind CSS
   - API client with JWT token attachment

3. **Documentation** (`/specs`)
   - Complete specifications
   - API contracts
   - Database schema
   - UI/UX guidelines

## Feature Breakdown

### F1: Authentication System

**Priority**: P1 (Blocking)

**Components**:
- Better Auth setup on frontend
- JWT issuing and session management
- JWT verification middleware on backend
- User ID extraction and validation
- Secure token storage

**Dependencies**: None

**See**: `specs/features/authentication.md`

---

### F2: Backend API Foundation

**Priority**: P1 (Blocking)

**Components**:
- FastAPI application setup
- SQLModel models and schemas
- Database connection and session management
- CORS configuration for localhost:3000
- Error handling and logging

**Dependencies**: None

**See**: `specs/database/schema.md`, `specs/api/rest-endpoints.md`

---

### F3: Task CRUD Operations

**Priority**: P1 (Core Feature)

**Components**:
- Create task endpoint
- List tasks endpoint with filters
- Get single task endpoint
- Update task endpoint
- Delete task endpoint
- Toggle completion endpoint

**Dependencies**: F1 (Authentication), F2 (Backend Foundation)

**See**: `specs/features/task-crud.md`

---

### F4: Frontend UI

**Priority**: P1 (Core Feature)

**Components**:
- App layout and navigation
- Login/signup pages
- Task list page with filters
- Create task page
- Edit task page
- Responsive components

**Dependencies**: F1 (Authentication), F3 (Task CRUD)

**See**: `specs/ui/pages.md`, `specs/ui/components.md`

---

### F5: Search and Filters

**Priority**: P2 (Enhancement)

**Components**:
- Search tasks by title/description
- Filter by completion status
- Sort by created_at, updated_at, title
- Clear filters functionality

**Dependencies**: F3 (Task CRUD), F4 (Frontend UI)

**See**: `specs/features/task-crud.md#US-2`

---

### F6: Testing Suite

**Priority**: P1 (Quality Gate)

**Components**:
- Backend API tests (pytest)
- Authorization tests
- User data isolation tests
- Manual frontend testing

**Dependencies**: All features

**See**: `specs/features/task-crud.md#Testing Requirements`

---

## Implementation Plan

### Phase 1: Backend Foundation (Week 1)

**Tasks**:
1. Set up FastAPI application structure
2. Define SQLModel models and schemas
3. Implement database connection
4. Create JWT verification middleware
5. Implement basic error handling

**Deliverables**:
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/schemas.py`
- `backend/app/db.py`
- `backend/app/auth.py`
- `backend/requirements.txt`

---

### Phase 2: Task API Implementation (Week 1-2)

**Tasks**:
1. Implement POST /api/{user_id}/tasks
2. Implement GET /api/{user_id}/tasks
3. Implement GET /api/{user_id}/tasks/{id}
4. Implement PUT /api/{user_id}/tasks/{id}
5. Implement DELETE /api/{user_id}/tasks/{id}
6. Implement PATCH /api/{user_id}/tasks/{id}/complete

**Deliverables**:
- `backend/app/api/tasks.py`
- All endpoints with JWT protection
- User ID validation on all routes

---

### Phase 3: Backend Testing (Week 2)

**Tasks**:
1. Set up pytest configuration
2. Write tests for all CRUD operations
3. Write authorization tests
4. Write user data isolation tests
5. Write validation tests

**Deliverables**:
- `backend/tests/conftest.py`
- `backend/tests/test_tasks.py`
- All tests passing

---

### Phase 4: Frontend Foundation (Week 2)

**Tasks**:
1. Set up Next.js application
2. Configure Tailwind CSS
3. Integrate Better Auth
4. Create API client with JWT
5. Set up routing structure

**Deliverables**:
- `frontend/app/layout.js`
- `frontend/app/page.js`
- `frontend/lib/api.js`
- `frontend/package.json`
- `frontend/tailwind.config.js`

---

### Phase 5: Frontend UI Implementation (Week 3)

**Tasks**:
1. Create Navbar component
2. Create TodoList component
3. Create TodoItem component
4. Create TodoForm component
5. Create TodoFilters component
6. Implement all pages (list, create, edit)

**Deliverables**:
- `frontend/components/*.js`
- `frontend/app/todos/page.js`
- `frontend/app/todos/new/page.js`
- `frontend/app/todos/[id]/page.js`

---

### Phase 6: Integration and Testing (Week 3)

**Tasks**:
1. Test backend-frontend integration
2. Test all user flows
3. Test error handling
4. Test responsive design
5. Fix bugs and polish UI

**Deliverables**:
- Fully working application
- All tests passing
- Documentation updated

---

## API Contract Summary

### Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | /api/{user_id}/tasks | Create task | JWT |
| GET | /api/{user_id}/tasks | List tasks | JWT |
| GET | /api/{user_id}/tasks/{id} | Get task | JWT |
| PUT | /api/{user_id}/tasks/{id} | Update task | JWT |
| DELETE | /api/{user_id}/tasks/{id} | Delete task | JWT |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion | JWT |

See `specs/api/rest-endpoints.md` for complete contract details.

## Database Schema Summary

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

See `specs/database/schema.md` for complete schema details.

## UI Pages Summary

- `/` - Home/landing page
- `/login` - Login page (Better Auth)
- `/signup` - Sign up page (Better Auth)
- `/todos` - Task list with filters
- `/todos/new` - Create task form
- `/todos/[id]` - Edit task form

See `specs/ui/pages.md` for complete UI details.

## Success Criteria

Phase II is complete when:
- [ ] All API endpoints implemented and tested
- [ ] JWT authentication working on all endpoints
- [ ] User data isolation verified
- [ ] Frontend UI complete and responsive
- [ ] All backend tests passing
- [ ] Manual frontend tests passing
- [ ] Application runs locally without errors
- [ ] Documentation complete and accurate
- [ ] Code follows all constitution principles

## Dependencies and Prerequisites

### Development Tools
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git
- Code editor (VS Code recommended)

### External Services
- Neon PostgreSQL account (free tier)
- Better Auth configuration

### Environment Setup
- Backend `.env` file with secrets
- Frontend `.env.local` file with secrets
- Database connection string
- Shared JWT secret between frontend and backend

## Risk Mitigation

### Technical Risks
1. **Better Auth integration complexity**
   - Mitigation: Follow official documentation, use community examples

2. **JWT verification issues**
   - Mitigation: Test with multiple scenarios, use standard libraries

3. **CORS configuration**
   - Mitigation: Set up early, test with frontend

4. **Database connection failures**
   - Mitigation: Implement SQLite fallback, test connection on startup

### Timeline Risks
1. **Scope creep**
   - Mitigation: Strictly follow specs, defer non-P1 features

2. **Testing delays**
   - Mitigation: Write tests alongside implementation (TDD)

3. **Integration issues**
   - Mitigation: Integrate early and often, test continuously

## Out of Scope (Future Phases)

The following features are explicitly OUT OF SCOPE for Phase II:

- Task categories or tags
- Task priorities
- Due dates and reminders
- File attachments
- Comments on tasks
- Task sharing or collaboration
- Team features
- Advanced search with operators
- Pagination
- Real-time updates
- Email notifications
- Mobile native apps
- Export/import functionality
- Dark mode
- Internationalization

These may be considered for Phase III or beyond.

## References

- Main Constitution: `.specify/memory/constitution.md`
- Architecture: `specs/architecture.md`
- Task CRUD: `specs/features/task-crud.md`
- Authentication: `specs/features/authentication.md`
- API Endpoints: `specs/api/rest-endpoints.md`
- Database Schema: `specs/database/schema.md`
- UI Pages: `specs/ui/pages.md`
- UI Components: `specs/ui/components.md`
