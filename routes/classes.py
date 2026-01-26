from fastapi import APIRouter, status, HTTPException, Depends
from dependencies import get_current_user, check_admin
from models.users import User
from models.classes import Class
from sqlmodel import Session, select
from db import get_session
from datetime import datetime, timezone
from schemas.classes import ClassRead, ClassCreate
from uuid import UUID
from typing import List
router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)

@router.get("/", response_model=List[ClassRead])
async def get_classes(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    statement = select(Class).where((Class.tier == user.tier) & (Class.date > datetime.now(timezone.utc)))
    classes = db.exec(statement).all()
    return classes

@router.post("/create", response_model=ClassRead, status_code=status.HTTP_201_CREATED)
async def create_class(class_create: ClassCreate, _: User = Depends(check_admin), db: Session = Depends(get_session)):
    class_new = Class(**class_create.model_dump(exclude_unset=True))
    db.add(class_new)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(class_new)

    return class_new

@router.delete("/delete/{class_id}", status_code=status.HTTP_204_NO_CONTENT)    
async def delete_class(class_id: UUID, _: User = Depends(check_admin), db: Session = Depends(get_session)):
    class_del = db.get(Class, class_id)
    if not class_del:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Class not found")
    db.delete(class_del)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    
    return