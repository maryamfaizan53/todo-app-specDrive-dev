# Feature: Authentication & Authorization

## Overview

Implement JWT-based authentication using Better Auth on the frontend and JWT verification on the backend to secure all API endpoints and ensure user data isolation.

## User Stories

### US-1: User Sign Up (Priority: P1)

**As a** new user
**I want to** create an account
**So that** I can start using the todo application

**Acceptance Criteria**:
- User can sign up with email and password
- Better Auth creates user record
- User is automatically logged in after sign up
- JWT token is issued upon successful sign up
- Frontend stores JWT securely
- Invalid email shows validation error
- Weak password shows validation error

**Implementation**: Handled by Better Auth library

---

### US-2: User Login (Priority: P1)

**As a** registered user
**I want to** log in to my account
**So that** I can access my tasks

**Acceptance Criteria**:
- User can log in with email and password
- Better Auth validates credentials
- JWT token is issued upon successful login
- Frontend stores JWT securely
- Invalid credentials show error message
- Frontend redirects to tasks page after login

**Implementation**: Handled by Better Auth library

---

### US-3: User Logout (Priority: P1)

**As a** logged-in user
**I want to** log out
**So that** I can protect my account

**Acceptance Criteria**:
- User can click logout button
- Frontend clears stored JWT
- Frontend redirects to login page
- Subsequent API requests fail with 401

**Implementation**: Handled by Better Auth library

---

### US-4: JWT Token Attachment (Priority: P1)

**As a** frontend application
**I want to** attach JWT token to all API requests
**So that** the backend can authenticate the user

**Acceptance Criteria**:
- All API requests include `Authorization: Bearer <token>` header
- Token is retrieved from Better Auth session
- Missing token results in API error
- Invalid token results in 401 response

**Implementation**: Custom API client in `frontend/lib/api.js`

**Code Pattern**:
```javascript
export async function apiRequest(endpoint, options = {}) {
  const token = getTokenFromAuth();

  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (response.status === 401) {
    window.location.href = '/login';
    return;
  }

  return response.json();
}
```

---

### US-5: JWT Token Verification (Priority: P1)

**As a** backend API
**I want to** verify JWT tokens on all protected endpoints
**So that** only authenticated users can access data

**Acceptance Criteria**:
- All task endpoints require valid JWT
- JWT signature is verified using `BETTER_AUTH_SECRET`
- `user_id` is extracted from JWT `sub` claim
- Invalid JWT returns 401 Unauthorized
- Missing JWT returns 401 Unauthorized
- Expired JWT returns 401 Unauthorized

**Implementation**: Custom dependency in `backend/app/auth.py`

**Code Pattern**:
```python
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
        return payload  # Contains user_id in "sub" claim
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

### US-6: User ID Validation (Priority: P1)

**As a** backend API
**I want to** validate that path `user_id` matches JWT `user_id`
**So that** users cannot access other users' data

**Acceptance Criteria**:
- All task endpoints validate `user_id` from path
- Path `user_id` must match JWT `sub` claim
- Mismatched `user_id` returns 403 Forbidden
- Validation happens before any database operation

**Implementation**: In every route handler

**Code Pattern**:
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
    # Proceed with task creation...
```

---

### US-7: Session Persistence (Priority: P2)

**As a** logged-in user
**I want to** stay logged in when I refresh the page
**So that** I don't have to log in repeatedly

**Acceptance Criteria**:
- JWT token is stored securely (localStorage or httpOnly cookie)
- Token is retrieved on page load
- User remains logged in until token expires or logout
- Expired token redirects to login

**Implementation**: Handled by Better Auth library

---

### US-8: Error Handling for Auth Failures (Priority: P1)

**As a** user
**I want to** see clear error messages when authentication fails
**So that** I understand what went wrong

**Acceptance Criteria**:
- 401 errors redirect to login page
- 403 errors show "Access denied" message
- Network errors show "Connection failed" message
- All errors are user-friendly (no technical details)

**Implementation**: In frontend API client and error boundaries

---

## Technical Requirements

### Frontend Configuration

**Environment Variables** (`.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<shared-secret-with-backend>
```

**Better Auth Setup**: Follow Better Auth documentation for Next.js integration

### Backend Configuration

**Environment Variables** (`.env`):
```
BETTER_AUTH_SECRET=<shared-secret-with-frontend>
DATABASE_URL=postgresql://user:password@host/dbname
CORS_ORIGINS=http://localhost:3000
```

**Dependencies** (`requirements.txt`):
```
fastapi
uvicorn
sqlmodel
pyjwt
python-dotenv
```

**CORS Configuration** (`backend/app/main.py`):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Considerations

### Token Security

1. **Never expose secret**: `BETTER_AUTH_SECRET` must be in `.env` only
2. **Use strong secret**: Minimum 32 characters, random
3. **Token expiration**: Set reasonable expiry (e.g., 24 hours)
4. **HTTPS in production**: Always use HTTPS for token transmission

### Data Protection

1. **User ID validation**: ALWAYS validate path user_id matches JWT user_id
2. **Database filtering**: ALWAYS filter queries by user_id
3. **Error messages**: Never expose internal errors or stack traces
4. **Rate limiting**: Consider rate limiting for auth endpoints (future)

### Testing Auth

**Backend Tests**:
```python
def test_missing_token():
    response = client.get("/api/user-123/tasks")
    assert response.status_code == 401

def test_invalid_token():
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/user-123/tasks", headers=headers)
    assert response.status_code == 401

def test_mismatched_user_id():
    token = create_jwt(user_id="user-123")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/user-456/tasks", headers=headers)
    assert response.status_code == 403

def test_valid_token():
    token = create_jwt(user_id="user-123")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/user-123/tasks", headers=headers)
    assert response.status_code == 200
```

**Frontend Tests** (Manual):
- [ ] Sign up creates account and logs in
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials shows error
- [ ] Logout clears session
- [ ] Logged out user redirected to login
- [ ] Token refresh works (if implemented)
- [ ] Expired token redirects to login

## Success Criteria

Authentication is complete when:
- [ ] Better Auth integrated on frontend
- [ ] JWT verification implemented on backend
- [ ] All protected endpoints require JWT
- [ ] User ID validation enforced on all routes
- [ ] 401/403 errors handled correctly
- [ ] All auth tests pass
- [ ] Users cannot access other users' data
- [ ] Security best practices followed
