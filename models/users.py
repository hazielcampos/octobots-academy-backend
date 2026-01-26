from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from utils.time import now_utc
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    pfp_url: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    tier: int = Field(default=0)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(
        default_factory=now_utc,
        sa_column_kwargs={"onupdate": now_utc}
    )