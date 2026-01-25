from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db import get_session
from auth.utils import decode_token
from models.users import User
from sqlmodel import select, Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Dependencies ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    print("Token recibido:", token)
    payload = decode_token(token)
    print("Payload decodificado:", payload)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user