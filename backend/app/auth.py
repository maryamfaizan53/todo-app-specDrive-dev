"""
JWT authentication middleware and dependencies.
"""
from fastapi import Depends, HTTPException, Header
import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get JWT secret from environment
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")


async def get_current_user(authorization: str = Header(None)) -> dict:
    """
    JWT verification dependency for protected routes.

    Extracts and validates JWT token from Authorization header,
    then returns the decoded payload containing user information.

    Args:
        authorization: Authorization header value (format: "Bearer <token>")

    Returns:
        dict: Decoded JWT payload containing user information
              Expected to have "id" field (from "sub" claim)

    Raises:
        HTTPException: 401 if token is missing, malformed, or invalid

    Usage:
        @router.get("/tasks")
        async def list_tasks(current_user: dict = Depends(get_current_user)):
            user_id = current_user["id"]
            # Use user_id for filtering
            pass
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected 'Bearer <token>'"
        )

    # Extract token from "Bearer <token>"
    token = authorization.split(" ")[1]

    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        # Extract user_id from "sub" claim (standard JWT claim)
        # Normalize to "id" for consistency in application code
        if "sub" in payload:
            payload["id"] = payload["sub"]
        elif "id" not in payload:
            raise HTTPException(
                status_code=401,
                detail="Token missing user identifier"
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
