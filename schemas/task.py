from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskRead(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
