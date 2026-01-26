from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from utils.time import now_utc
from sqlmodel import SQLModel, Field, Column, TEXT

class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    str_id: str = Field(index=True, unique=True)
    title: str = Field(index=True)
    tmb_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    content: str = Field(default=None, sa_column=Column(TEXT))
    tier: int = Field(default=0)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(
        default_factory=now_utc,
        sa_column_kwargs={"onupdate": now_utc}
    )

class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(default=None)
    order: int = Field(default=None)
    content: str = Field(default=None, sa_column=Column(TEXT))
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(
        default_factory=now_utc,
        sa_column_kwargs={"onupdate": now_utc}
    )

class CourseProgress(SQLModel, table=True):
    __tablename__ = "course_progress"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    course_id: UUID = Field(default=None)
    user_ud: UUID = Field(default=None)