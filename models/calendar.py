from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from utils.time import now_utc
from sqlmodel import SQLModel, Field

class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    description: Optional[str] = Field(default=None)
    date: datetime = Field(default=None)
    room_id: str = Field(default=None)
    room_password: str = Field(default=None)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(
        default_factory=now_utc,
        sa_column_kwargs={"onupdate": now_utc}
    )