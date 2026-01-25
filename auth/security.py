from sqlmodel import Session, select
from models.users import User
from auth.utils import check_password

def authenticate_user(db: Session, username: str, password: str):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if not user or not check_password(password, user.password_hash):
        return None
    return user