from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ClassCreate(BaseModel):
    name: str
    description: UUID
    date: datetime
    room_id: str
    room_password: Optional[str] = None
    tier: Optional[int] = 0

class ClassUpdate(BaseModel):
    name: str
    description: UUID
    date: datetime
    room_id: str
    room_password: Optional[str] = None
    tier: Optional[int] = 0

class ClassRead(BaseModel):
    id: UUID
    name: str
    description: UUID
    date: datetime
    room_id: str
    room_password: Optional[str] = None
    tier: Optional[int] = 0
    created_at: datetime