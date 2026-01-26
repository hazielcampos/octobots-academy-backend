from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    pfp_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None

class UserUpdateAdmin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    pfp_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    tier: Optional[int] = None
    is_admin: Optional[bool] = None

class UserUpdateStatus(BaseModel):
    is_active: bool

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    pfp_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    tier: int
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str