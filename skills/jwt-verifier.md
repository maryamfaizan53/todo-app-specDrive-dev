---
name: jwt-verifier
description: Verify and decode JWT tokens given a secret or JWKS endpoint. Returns token claims or verification error.
inputs:
- token: string
- secret_or_jwks: string
outputs:
- claims: object
- error: string (nullable)
usage: Used by auth-integration and backend-impl to validate tokens and extract `user_id`.
---
