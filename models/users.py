from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

def now_utc():
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    created_at: datetime = Field(default_factory=now_utc)
    updated_at: Optional[datetime] = Field(default=None)