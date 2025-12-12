<!--
SYNC IMPACT REPORT
==================
Version Change: 0.0.0 → 1.0.0
Rationale: Initial constitution for Phase II Todo Full-Stack Web Application

Principles Added:
- I. Spec-Driven Development (SDD)
- II. JWT Authentication & Authorization
- III. User Data Isolation
- IV. Test-First Development
- V. API Contract Validation
- VI. Frontend-Backend Integration
- VII. Database Migrations Safety
- VIII. Observability & Error Handling

Sections Added:
- Technology Stack
- Development Workflow
- Governance

Templates Status:
✅ plan-template.md - Constitution Check section aligns with principles
✅ spec-template.md - User stories and requirements format compatible
✅ tasks-template.md - Task categorization aligns with principles
✅ All command files - No agent-specific references to update

Follow-up TODOs:
- None - all placeholders filled

Last Updated: 2025-12-12
-->

# Phase II Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All implementation work MUST begin with complete specifications under `/specs`. No code shall be written without first reading and validating:
- `specs/overview.md` - Project overview and goals
- `specs/architecture.md` - System architecture decisions
- `specs/todo.constitution.md` - Domain-specific rules
- `specs/features/*.md` - Feature specifications
- `specs/api/rest-endpoints.md` - API contracts
- `specs/database/schema.md` - Data models
- `specs/ui/*.md` - UI/UX requirements

**Rationale**: Spec-driven development prevents scope creep, ensures alignment with requirements, and creates traceable implementation paths. All code changes must reference their originating spec.

### II. JWT Authentication & Authorization

ALL API endpoints MUST enforce JWT-based authentication and authorization. No endpoint shall accept requests without valid JWT tokens except public endpoints explicitly marked in specs.

**Non-negotiable rules**:
- Better Auth integration required on frontend
- JWT verification middleware required on all protected FastAPI endpoints
- Path `user_id` MUST match JWT token `user_id` claim
- Unauthorized requests return HTTP 401
- Forbidden requests (user_id mismatch) return HTTP 403

**Rationale**: Security is paramount. User data must be protected through proper authentication and authorization at every layer.

### III. User Data Isolation

All task queries and operations MUST be filtered by authenticated `user_id`. Users shall NEVER access, view, or modify data belonging to other users.

**Enforcement points**:
- Database queries filtered by `user_id`
- API endpoints validate path `user_id` matches JWT claim
- Frontend sends `user_id` in API requests based on authenticated session
- Tests validate cross-user data isolation

**Rationale**: Multi-tenant data isolation is a security requirement. Data leaks between users are unacceptable and must be prevented at the database and API layers.

### IV. Test-First Development

Tests MUST be written BEFORE implementation for all new features. The Red-Green-Refactor cycle is mandatory:
1. **Red**: Write tests that define expected behavior - tests MUST fail initially
2. **Green**: Implement minimal code to make tests pass
3. **Refactor**: Improve code while keeping tests green

**Test coverage requirements**:
- Contract tests for all API endpoints
- Integration tests for user journeys
- Unit tests for business logic and data transformations
- Authorization tests (invalid/missing JWT, user_id mismatch)

**Rationale**: Test-first development catches bugs early, documents expected behavior, and enables confident refactoring. Tests serve as executable specifications.

### V. API Contract Validation

All REST endpoints MUST conform to specifications in `specs/api/rest-endpoints.md`. API contracts are non-negotiable and include:
- Exact HTTP methods and paths
- Request/response schemas (Pydantic/SQLModel)
- Status codes for success and error cases
- Authentication requirements
- Example curl commands for testing

**Contract change process**:
- Update spec FIRST
- Update implementation to match
- Update tests to validate new contract
- Document breaking changes in ADR

**Rationale**: API contracts are agreements between frontend and backend. Breaking changes without documentation cause integration failures and deployment issues.

### VI. Frontend-Backend Integration

Frontend (Next.js) and Backend (FastAPI) MUST integrate through well-defined API contracts with proper error handling:

**Frontend requirements**:
- API client (`frontend/lib/api.js`) with JWT token attachment
- `Authorization: Bearer <token>` header on all authenticated requests
- Proper error handling for 401, 403, 404, 422, 500 responses
- Loading states and user feedback for async operations

**Backend requirements**:
- CORS configuration for `http://localhost:3000`
- Consistent error response format
- Request validation with detailed error messages
- Rate limiting and request size limits

**Rationale**: Clean separation of concerns between frontend and backend enables parallel development and independent deployment. Proper error handling creates better user experience.

### VII. Database Migrations Safety

All database schema changes MUST use safe migration practices with Neon-compatible SQL:

**Migration requirements**:
- SQLModel models define schema
- Migrations are incremental and reversible
- Rollback SQL provided for each migration
- No destructive changes without backup strategy
- Schema changes tested in development before production

**Safety checks**:
- No data loss on migration
- Backward compatibility maintained during rollout
- Migration tested with realistic data volume

**Rationale**: Database migrations in production are high-risk operations. Safe, reversible migrations with rollback plans prevent data loss and downtime.

### VIII. Observability & Error Handling

All components MUST implement comprehensive logging, error handling, and monitoring:

**Logging requirements**:
- Structured logging with consistent format
- Request/response logging for API calls
- Error logging with stack traces
- Performance metrics (latency, throughput)
- Security events (auth failures, unauthorized access attempts)

**Error handling requirements**:
- Never expose internal errors to users
- Detailed error messages in logs, generic messages to clients
- Proper HTTP status codes
- Error recovery and graceful degradation

**Rationale**: Observability enables debugging, performance optimization, and security monitoring. Proper error handling prevents information leakage and improves user experience.

## Technology Stack

**Backend**:
- Python 3.11+
- FastAPI (web framework)
- SQLModel (ORM and Pydantic schemas)
- Neon Postgres (database)
- Uvicorn (ASGI server)
- PyJWT (JWT verification)

**Frontend**:
- Node.js 18+ / npm
- Next.js 14+ (App Router)
- JavaScript (not TypeScript per spec)
- Tailwind CSS (styling)
- Better Auth (authentication)

**Development Tools**:
- pytest (backend testing)
- Git (version control)
- Environment variables (.env files for secrets)

**Constraints**:
- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`
- Database connection via Neon connection string
- JWT secrets stored in environment variables

## Development Workflow

**Implementation Flow**:
1. Read all relevant specs under `/specs`
2. Create/update implementation plan (`/sp.plan`)
3. Generate actionable tasks (`/sp.tasks`)
4. Write tests FIRST (Red phase)
5. Implement features (Green phase)
6. Refactor and optimize (Refactor phase)
7. Create Prompt History Records (PHRs) for all work
8. Suggest ADRs for architectural decisions

**Code Review Requirements**:
- All code references originating specs
- Tests pass and provide meaningful coverage
- No security vulnerabilities (SQL injection, XSS, command injection, etc.)
- Follow principle of least privilege
- Secrets never hardcoded
- Smallest viable change (no unnecessary refactoring)

**Quality Gates**:
- All tests pass
- Code adheres to constitution principles
- API contracts validated
- User data isolation verified
- Authentication and authorization working
- Documentation updated

## Governance

This constitution supersedes all other development practices and guidelines. All code, PRs, and reviews MUST verify compliance with these principles.

**Amendment Process**:
1. Proposed changes documented with rationale
2. Version increment following semantic versioning:
   - MAJOR: Breaking principle removals or incompatible changes
   - MINOR: New principles or expanded guidance
   - PATCH: Clarifications, typo fixes, non-semantic refinements
3. Sync impact analysis across dependent templates
4. Approval required before implementation
5. Migration plan for existing code if needed

**Version Management**:
- All changes update version, ratification/amendment dates
- Sync Impact Report created for each update
- Dependent templates checked and updated
- Follow-up actions documented

**Compliance Review**:
- All PRs verify alignment with constitution
- Complexity violations require explicit justification
- Security reviews for authentication/authorization changes
- Architecture reviews for database schema changes

**Runtime Guidance**:
- See `/CLAUDE.md` for agent-level development guidance
- See `/frontend/CLAUDE.md` for frontend-specific guidance
- See `/backend/CLAUDE.md` for backend-specific guidance
- See `.specify/templates/` for artifact templates

**Version**: 1.0.0 | **Ratified**: 2025-12-12 | **Last Amended**: 2025-12-12
