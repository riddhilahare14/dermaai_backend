# modules/users/schemas.py
from pydantic import BaseModel, EmailStr, Field

# -------------------- Input schema for creating a user --------------------
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "patient"  # default to patient
    email: EmailStr
    phone_number: str | None = None

# -------------------- Output schema --------------------
class UserOut(BaseModel):
    id: int
    username: str
    role: str
    email: EmailStr
    phone_number: str | None = None

    model_config = {"from_attributes": True}

