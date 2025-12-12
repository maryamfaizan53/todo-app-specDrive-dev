---
id: 001
title: Phase II Todo Constitution Creation
stage: constitution
date: 2025-12-12
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: Maryam Faizan
command: /sp.constitution
labels: ["constitution", "governance", "phase-2", "fullstack", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

You are Claude Code working in a monorepo for Hackathon II – Evolution of Todo (Phase II).

## GOAL

Implement the complete **Phase II: Todo Full-Stack Web Application** using Spec-Driven Development.

You MUST:

- Read and respect all specs under `/specs`.
- Implement a full **frontend** (Next.js App Router + Tailwind + JS) in `/frontend`.
- Implement a full **backend** (FastAPI + SQLModel + Neon-ready) in `/backend`.
- Implement Better Auth integration with JWT so that FastAPI can authenticate and authorize all requests.
- Implement all REST endpoints and UI behaviors described in the specs.

## REPO STRUCTURE

The repo root contains:

- `.spec-kit/config.yaml`
- `specs/`
  - `overview.md`
  - `architecture.md`
  - `todo.constitution.md`
  - `features/task-crud.md`
  - `features/authentication.md`
  - `features/phase2-fullstack-todo.md`  (master Phase II spec)
  - `api/rest-endpoints.md`
  - `database/schema.md`
  - `ui/components.md`
  - `ui/pages.md`
- `CLAUDE.md`               (root guidelines)
- `frontend/CLAUDE.md`      (frontend guidelines)
- `backend/CLAUDE.md`       (backend guidelines)
- `frontend/`               (Next.js app – may be partially scaffolded)
- `backend/`                (FastAPI app – may be partially scaffolded)

YOU SHOULD INSPECT THESE FILES BEFORE CODING:
- `@specs/overview.md`
- `@specs/todo.constitution.md`
- `@specs/architecture.md`
- `@specs/features/task-crud.md`
- `@specs/features/authentication.md`
- `@specs/features/phase2-fullstack-todo.md`
- `@specs/api/rest-endpoints.md`
- `@specs/database/schema.md`
- `@specs/ui/components.md`
- `@specs/ui/pages.md`
- `@frontend/CLAUDE.md`
- `@backend/CLAUDE.md`

## TECHNOLOGY CONSTRAINTS

Backend: FastAPI + SQLModel + Neon Postgres + JWT
Frontend: Next.js + Tailwind + JavaScript + Better Auth

ENABLED AGENTS

The following subagents are registered and should be invoked automatically when relevant:

plan — Create implementation plans for features and refactors
research — Search for libraries, methods, best practices
db-designer — Create SQLModel models and DB migrations
api-designer — Define REST routes and schemas
backend-impl — Implement FastAPI endpoints, services, and tests
frontend-impl — Implement Next.js pages, forms, API clients
auth-integration — Setup Better Auth and JWT verification
test-and-qa — Create test plans, write tests, configure CI

REQUIRED SKILLS

These reusable Claude skills are invoked by agents:

web-search — for external docs
repo-reader — for reading file context
code-refactor — for generating patch diffs
schema-generator — for DB changes
jwt-verifier — for auth token parsing
db-migrator — for Neon-safe migration steps
http-tester — for API tests
doc-generator — for spec and doc writing

## Response snapshot

Created the Phase II Todo Full-Stack Web Application Constitution (v1.0.0) with 8 core principles:

1. **Spec-Driven Development (SDD)** - All implementation must start with complete specs under `/specs`
2. **JWT Authentication & Authorization** - All API endpoints enforce JWT-based auth with Better Auth integration
3. **User Data Isolation** - All queries filtered by authenticated user_id to prevent cross-user data access
4. **Test-First Development** - Mandatory Red-Green-Refactor cycle with tests written before implementation
5. **API Contract Validation** - REST endpoints must conform to `specs/api/rest-endpoints.md`
6. **Frontend-Backend Integration** - Next.js and FastAPI integrate through well-defined API contracts
7. **Database Migrations Safety** - Neon-compatible SQL migrations with rollback plans
8. **Observability & Error Handling** - Comprehensive logging and structured error handling

Added sections:
- **Technology Stack** - Python 3.11+, FastAPI, SQLModel, Neon Postgres, Next.js 14+, Tailwind, Better Auth
- **Development Workflow** - 8-step implementation flow with quality gates
- **Governance** - Amendment process, version management, compliance review

All template files verified for consistency. No placeholders remaining. Constitution file includes Sync Impact Report documenting the v1.0.0 creation.

## Outcome

- ✅ Impact: Created foundational governance document for Phase II Todo application with 8 core principles covering security, testing, API contracts, and development workflow
- 🧪 Tests: N/A (constitution document, not code)
- 📁 Files: .specify/memory/constitution.md (created), history/prompts/constitution/001-phase2-todo-constitution-creation.constitution.prompt.md (this PHR)
- 🔁 Next prompts: Read spec files, create implementation plan (/sp.plan), generate tasks (/sp.tasks), or begin implementation
- 🧠 Reflection: Constitution establishes clear guardrails for full-stack development with emphasis on security (JWT auth, user data isolation), testing (test-first), and contract validation (API specs). All 8 agents now have clear principles to follow.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All placeholders filled, version set to 1.0.0, sync report included, no template inconsistencies
- Prompt variant (if applicable): Standard constitution creation workflow
- Next experiment (smallest change to try): Validate constitution principles during /sp.plan execution to ensure plan adheres to SDD and test-first requirements
