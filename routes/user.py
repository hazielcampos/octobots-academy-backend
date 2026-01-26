from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_current_user
from models.users import User
from sqlmodel import Session, select
from db import get_session
from schemas.user import UserUpdate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserRead])
async def get_users(user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    users = db.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}")
async def update_user(user_id: int, user_updated: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """ Check if the target is the same as the current user """ 
    if user.id != user_id and user.is_admin is False:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_updated.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """ Check if the target is the same as the current user """ 
    if user.id != user_id and user.is_admin is False:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}