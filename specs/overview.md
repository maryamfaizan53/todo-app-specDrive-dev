# Phase II: Todo Full-Stack Web Application - Overview

## Project Purpose

Build a complete, production-ready Full-Stack Todo Web Application that demonstrates:
- Modern web development practices with Next.js and FastAPI
- Secure JWT-based authentication and authorization
- Multi-tenant data isolation
- RESTful API design
- Test-driven development

## Goals

1. **Authentication & Authorization**: Implement Better Auth with JWT issuing for secure user authentication
2. **User-specific Tasks**: Complete CRUD operations with data isolation per user
3. **Rich Features**: Filters, sorting, search, and task completion toggle
4. **Responsive Frontend**: Clean, mobile-first UI using Tailwind CSS
5. **Secure API**: JWT-protected FastAPI backend with user validation
6. **Persistent Storage**: Neon PostgreSQL with SQLite fallback for development
7. **Monorepo Architecture**: Well-organized frontend and backend structure
8. **Test Automation**: Comprehensive API and unit tests

## Technology Stack

### Frontend
- Next.js 14+ (App Router) with JavaScript
- Tailwind CSS v3+ for styling
- Better Auth for authentication and JWT issuing
- Runs on `http://localhost:3000`

### Backend
- FastAPI (latest stable) with SQLModel ORM
- Neon PostgreSQL (auto-fallback to SQLite for local dev)
- PyJWT for JWT verification
- Uvicorn ASGI server
- Runs on `http://localhost:8000`

### Testing
- pytest for backend tests
- Manual testing for frontend

## Non-Goals

- No TypeScript (JavaScript only per spec)
- No custom JWT library (use PyJWT with official patterns)
- No additional cloud services beyond Neon
- No server-side rendering overrides beyond Next.js defaults

## Success Criteria

A feature is considered successful when:
1. It matches the specification exactly
2. Returns correct responses with proper status codes
3. Uses JWT-based authentication properly
4. Restricts all data to the authenticated user
5. Works seamlessly in the Next.js frontend
6. Passes all automated tests
7. Follows all constitution principles
