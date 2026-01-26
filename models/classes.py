from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from utils.time import now_utc
from sqlmodel import SQLModel, Field

class Class(SQLModel, table=True):
    __tablename__ = "classes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    date: datetime = Field(default=None)
    room_id: str = Field(default=None)
    room_password: str = Field(default=None)
    tier: int = Field(default=0)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(
        default_factory=now_utc,
        sa_column_kwargs={"onupdate": now_utc}
    )