# Todo Application Constitution

## Domain Rules

### Task Management Rules

1. **Task Ownership**: Every task MUST belong to exactly one user
   - Tasks cannot be shared between users
   - Tasks cannot be transferred to another user
   - Orphaned tasks (no user_id) are not allowed

2. **Task Properties**:
   - `title`: Required, non-empty string (max 255 characters)
   - `description`: Optional string (max 2000 characters)
   - `completed`: Required boolean, defaults to `false`
   - `created_at`: Auto-generated timestamp
   - `updated_at`: Auto-updated timestamp

3. **Task Operations**:
   - **Create**: User can create unlimited tasks
   - **Read**: User can only view their own tasks
   - **Update**: User can only update their own tasks
   - **Delete**: User can only delete their own tasks
   - **Complete**: User can toggle completion status of their own tasks

4. **Task Listing**:
   - Default: Show all tasks (completed and incomplete)
   - Filter by: completed status, date range, search query
   - Sort by: created_at, updated_at, title
   - No pagination required (for simplicity in Phase II)

### User Rules

1. **User Identity**:
   - Users identified by unique `user_id` from Better Auth
   - `user_id` must match JWT token `sub` claim
   - No anonymous task creation allowed

2. **User Authentication**:
   - All operations require valid JWT token
   - JWT must not be expired
   - JWT must be signed with correct secret

3. **User Authorization**:
   - Users can ONLY access their own data
   - Path `user_id` must match authenticated `user_id`
   - Cross-user access returns 403 Forbidden

### Data Validation Rules

1. **Input Validation**:
   - Required fields must be present
   - String lengths must not exceed limits
   - Invalid data returns 422 Unprocessable Entity

2. **Output Consistency**:
   - All timestamps in ISO 8601 format
   - Boolean values as true/false (not 0/1)
   - Null values for optional empty fields

3. **Error Responses**:
   - 400: Bad request format
   - 401: Missing or invalid authentication
   - 403: Forbidden (user_id mismatch)
   - 404: Resource not found
   - 422: Validation error
   - 500: Internal server error

### Security Rules

1. **Authentication Required**:
   - All task endpoints require JWT
   - No public endpoints for task operations
   - Token must be in `Authorization: Bearer <token>` header

2. **Authorization Enforcement**:
   - Backend validates user_id on every request
   - Database queries always filter by user_id
   - No direct database access from frontend

3. **Data Protection**:
   - Secrets stored in environment variables only
   - No secrets in code or version control
   - CORS restricted to localhost:3000 (dev) or production domain

### Business Logic Rules

1. **Task Completion**:
   - Toggling completion updates `updated_at`
   - Completed tasks remain in list (no auto-archiving)
   - Can toggle completion multiple times

2. **Task Deletion**:
   - Deletion is permanent (no soft delete in Phase II)
   - Deleted tasks cannot be recovered
   - Frontend should confirm before deletion

3. **Search and Filter**:
   - Search matches title and description (case-insensitive)
   - Filters are combinable (e.g., completed + search)
   - Empty results return empty array (not 404)

### Testing Rules

1. **Test Coverage Required**:
   - All CRUD operations
   - All authorization scenarios (valid, invalid, mismatched user_id)
   - All validation scenarios (missing fields, invalid data)
   - All filter and search scenarios

2. **Test Data Isolation**:
   - Each test uses separate user_id
   - Tests clean up after themselves
   - No shared test data between tests

3. **Test Assertions**:
   - Verify response status codes
   - Verify response body structure
   - Verify database state changes
   - Verify user_id filtering works

## Implementation Constraints

1. **Technology Constraints**:
   - JavaScript only (no TypeScript)
   - No custom authentication (must use Better Auth)
   - No custom ORM queries (use SQLModel patterns)
   - No custom CSS (use Tailwind utilities)

2. **Scope Constraints**:
   - Single user per session
   - No task sharing or collaboration
   - No task categories or tags
   - No file attachments
   - No comments on tasks
   - No task priorities
   - No due dates
   - No notifications

3. **Performance Constraints**:
   - No pagination required (assume < 1000 tasks per user)
   - No caching required
   - No rate limiting required (development only)

## Maintenance Rules

1. **Code Quality**:
   - Follow constitution principles
   - Write tests before implementation
   - Keep functions small and focused
   - Use descriptive variable names

2. **Documentation**:
   - API endpoints match spec exactly
   - Code references originating spec
   - PHRs created for all significant work

3. **Version Control**:
   - Commit after each completed task
   - Use descriptive commit messages
   - Reference spec or task number in commits
