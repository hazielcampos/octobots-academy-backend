from fastapi import APIRouter, Depends, HTTPException, status, Response
from schemas.user import UserCreate, UserRead, UserRead
from fastapi.security import OAuth2PasswordRequestForm
from auth.security import authenticate_user
from auth.utils import create_access_token, hash_password
from sqlmodel import Session, select
from db import get_session
from models.users import User
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(days=30))
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # solo HTTPS
        samesite="strict",
        max_age=86400
    )
    return {"message": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="strict",
        secure=True  # solo HTTPS
    )
    return {"message": "Logout successful"}

@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate, db: Session = Depends(get_session)):
    statement = select(User).where((User.username == user_create.username) | (User.email == user_create.email))
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=hash_password(user_create.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user