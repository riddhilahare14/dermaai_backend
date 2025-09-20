# modules/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from passlib.context import CryptContext
from modules.core.db import get_db
from modules.users.models import User
from modules.patients.models import Patient
from modules.doctors.models import Doctor
from modules.auth.security import create_access_token, get_current_user
from modules.auth.schemas import UserCreate, LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 👇 Automatically create patient/doctor entry
    if new_user.role == "patient":
        patient = Patient(user_id=new_user.id)
        db.add(patient)
        db.commit()

    elif new_user.role == "doctor":
        doctor = Doctor(user_id=new_user.id)
        db.add(doctor)
        db.commit()

    return {"msg": f"User {new_user.username} created successfully", "role": new_user.role}


# -------------------- LOGIN --------------------
@router.post("/login")
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter((User.username == form_data.username_or_email) | (User.email == form_data.username_or_email))
        .first()
    )

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username/email or password")

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(hours=24),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# -------------------- PROFILE --------------------
@router.get("/profile")
def read_profile(current_user=Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "phone_number": current_user.phone_number,
    }
