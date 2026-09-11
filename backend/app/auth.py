"""
Staff authentication for internal/admin endpoints (currently: GET /api/leads
and GET /api/leads/access-log).

Replaces the earlier shared-API-key approach with real per-staff-member
accounts:
  - Each staff member has their own username + password (bcrypt-hashed,
    never stored in plain text).
  - POST /api/auth/login exchanges valid credentials for a short-lived JWT.
  - Protected routes require that JWT in an `Authorization: Bearer <token>`
    header and resolve it back to a specific staff user on every request.
  - Every successful read of the leads list is logged with that user's
    username and a timestamp (see crud.log_lead_access), giving a real
    audit trail — "who looked at the leads, and when" — instead of just
    "someone with the shared key".

Setup (one-time):
    Add this line to backend/.env (create the file if it doesn't exist):
        JWT_SECRET_KEY=<a long random string>
    Generate one with:
        python -c "import secrets; print(secrets.token_urlsafe(32))"

    Then:
    python -m app.create_staff --username jane --full-name "Jane Doe"
    (you'll be prompted for a password)

Then log in:
    curl -X POST http://localhost:8000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"username": "jane", "password": "..."}'
    # -> {"access_token": "...", "token_type": "bearer", "expires_in": 3600}

And call protected routes with the token:
    curl http://localhost:8000/api/leads \
      -H "Authorization: Bearer <access_token>"

Fails safe: if JWT_SECRET_KEY isn't set, protected routes refuse to work
rather than silently running without real protection.
"""
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from . import crud, models
from . database import get_db

# Load backend/.env as soon as this module is imported, so JWT_SECRET_KEY
# is available regardless of whether the terminal session set it manually.
# This does NOT overwrite a variable that's already set in the real
# environment (e.g. on a production host) — os.environ wins if present.
load_dotenv()

JWT_SECRET_ENV_VAR = "JWT_SECRET_KEY"
JWT_ALGORITHM = "HS256"
DEFAULT_TOKEN_LIFETIME_MINUTES = 60

_bearer_scheme = HTTPBearer(auto_error=False)


def _get_jwt_secret() -> str:
    secret = os.environ.get(JWT_SECRET_ENV_VAR)
    if not secret:
        raise RuntimeError(
            f"{JWT_SECRET_ENV_VAR} is not set. Refusing to start with unprotected "
            "internal endpoints. Add this line to backend/.env:\n"
            f"    {JWT_SECRET_ENV_VAR}=<a long random string>\n"
            "Generate one with:\n"
            '    python -c "import secrets; print(secrets.token_urlsafe(32))"'
        )
    return secret


# ---------- Password hashing ----------

def hash_password(plain_password: str) -> str:
    """Bcrypt-hash a plain-text password for storage."""
    # bcrypt has a 72-byte input limit; truncate deliberately rather than
    # letting the library raise on unusually long input.
    pw_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))
    except ValueError:
        # malformed hash in the DB — treat as "does not match" rather than 500
        return False


# ---------- JWT issuing ----------

def create_access_token(username: str, expires_minutes: int = DEFAULT_TOKEN_LIFETIME_MINUTES) -> tuple[str, int]:
    """Returns (token, expires_in_seconds)."""
    secret = _get_jwt_secret()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub": username,
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
    expires_in = int((expire - now).total_seconds())
    return token, expires_in


def authenticate_staff(db: Session, username: str, password: str) -> models.StaffUser | None:
    """Returns the StaffUser if credentials are valid and the account is active, else None."""
    staff = crud.get_staff_by_username(db, username)
    if not staff or not staff.is_active:
        return None
    if not verify_password(password, staff.hashed_password):
        return None
    return staff


# ---------- Dependency for protected routes ----------

def get_current_staff_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> models.StaffUser:
    """
    FastAPI dependency: validates the bearer JWT and resolves it to an
    active StaffUser. Raises 401 for any failure (missing token, expired,
    malformed, unknown user, deactivated account) — deliberately vague in
    the error detail so we don't hand out hints about which part failed.
    """
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or not credentials.credentials:
        raise unauthorized

    secret = _get_jwt_secret()
    try:
        payload = jwt.decode(credentials.credentials, secret, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired, please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise unauthorized

    username = payload.get("sub")
    if not username:
        raise unauthorized

    staff = crud.get_staff_by_username(db, username)
    if not staff or not staff.is_active:
        raise unauthorized

    return staff