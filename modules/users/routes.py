# modules/users/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from modules.auth.security import get_current_user
from modules.core.db import get_db
from modules.users.models import User

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------- GET ALL USERS (admin only) --------------------
@router.get("/")
def read_all_users(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(User).all()


# -------------------- GET SINGLE USER --------------------
@router.get("/{username}")
def read_user(username: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Allow self-view or admin-view
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    return user


# -------------------- GET USERS BY ROLE (admin only) --------------------
@router.get("/role/{role}")
def read_users_by_role(role: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(User).filter(User.role == role).all()


# -------------------- UPDATE USER ROLE (admin only) --------------------
@router.put("/{username}/role")
def update_role(username: str, new_role: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"msg": f"{username}'s role updated to {new_role}"}


# -------------------- UPDATE OWN PASSWORD --------------------
@router.put("/{username}/password")
def update_password(username: str, new_password: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return {"msg": "Password updated successfully"}


# -------------------- DELETE USER (admin only) --------------------
@router.delete("/{username}")
def delete(username: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"msg": f"User {username} deleted successfully"}
