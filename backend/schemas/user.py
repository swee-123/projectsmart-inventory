from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

# ✅ Allowed roles
RoleLiteral = Literal["Admin", "Manager", "Staff"]


# ✅ Schema for signup
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)
    role: RoleLiteral = "Staff"


# ✅ Schema for login
class UserLogin(BaseModel):
    username: str
    password: str


# ✅ Schema for reading user (used in /signup response)
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleLiteral

    # ✅ Required for ORM conversion (Pydantic v2 fix)
    model_config = {
        "from_attributes": True
    }


# ✅ Token response schema
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
