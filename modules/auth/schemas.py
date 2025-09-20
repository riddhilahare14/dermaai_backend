# modules/auth/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str | None = None  # optional
    password: str
    role: str = "patient"

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

