# modules/users/crud.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from modules.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- CREATE --------------------
def create_user(db: Session, username: str, password: str, role: str = "patient"):
    hashed_password = pwd_context.hash(password)
    new_user = User(
        username=username,
        hashed_password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# -------------------- READ --------------------
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session):
    return db.query(User).all()

def get_users_by_role(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()

# -------------------- UPDATE --------------------
def update_user_role(db: Session, username: str, new_role: str):
    user = get_user_by_username(db, username)
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
    return user

def update_user_password(db: Session, username: str, new_password: str):
    user = get_user_by_username(db, username)
    if user:
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        db.refresh(user)
    return user

# -------------------- DELETE --------------------
def delete_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if user:
        db.delete(user)
        db.commit()
    return user
