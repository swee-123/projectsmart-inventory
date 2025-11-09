from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User, UserRole
from backend.schemas.user import (
    UserCreate,
    UserLogin,
    UserRead,
    TokenResponse
)
from backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter()


# ✅ Signup endpoint
@router.post("/signup", response_model=UserRead, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # Check duplicates
    existing = db.query(User).filter(
        (User.username == payload.username) |
        (User.email == payload.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    # Create user
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=UserRole(payload.role)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ✅ Login endpoint (returns JWT)
@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create token with roles
    access_token = create_access_token(
        sub=str(user.id),
        roles=[user.role.value]
    )

    return TokenResponse(access_token=access_token)


# ✅ Authenticated user info
@router.get("/me")
def me(claims=Depends(get_current_user)):
    return {
        "sub": claims.get("sub"),
        "roles": claims.get("roles"),
        "aud": claims.get("aud"),
        "iss": claims.get("iss"),
        "exp": claims.get("exp"),
    }
