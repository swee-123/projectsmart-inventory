import os 
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.utils.azure_helpers import get_secret
from backend.utils.config import settings


# ✅ Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Bearer token extractor (Authorization: Bearer <token>)
bearer_scheme = HTTPBearer(auto_error=False)

# ✅ JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ✅ Secret key (from Key Vault OR local .env)
def _jwt_secret() -> str:
    secret = get_secret("JWT-SECRET", fallback_env="JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT secret not found (Key Vault or JWT_SECRET_KEY env needed).")
    return secret


# ✅ Password utils
def hash_password(password: str) -> str:
    # ✅ Fix: Prevent bcrypt crash for >72 byte passwords
    if len(password) > 50:   # 50 chars safe limit (bcrypt max is 72 bytes)
        raise HTTPException(
            status_code=400,
            detail="Password too long. Maximum 50 characters allowed."
        )

    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# ✅ JWT creation
def create_access_token(sub: str, roles: List[str]) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": sub,              # user id
        "roles": roles,          # Admin / Manager / Staff
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": settings.APP_NAME,
        "aud": settings.JWT_AUDIENCE,
    }

    return jwt.encode(payload, _jwt_secret(), algorithm=ALGORITHM)


# ✅ Decode + validate JWT
def decode_token(token: str) -> Dict[str, Any]:
    try:
        claims = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=[ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.APP_NAME,
        )
        return claims
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# ✅ Extract the current user from Authorization header
async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict[str, Any]:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = creds.credentials
    return decode_token(token)


# ✅ RBAC Role Checker
def require_role(*allowed_roles: str):
    allowed = set(map(str.lower, allowed_roles))

    async def checker(claims: Dict[str, Any] = Depends(get_current_user)):
        roles = claims.get("roles", [])
        if isinstance(roles, str):
            roles = [roles]

        roles_lower = set(map(str.lower, roles))

        if not roles_lower.intersection(allowed):
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")

        return claims

    return checker
