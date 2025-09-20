# modules/patients/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from modules.core.db import get_db
from modules.auth.security import get_current_user
from modules.users.models import User
from modules.patients import crud, schemas
from modules.core import cloudinary_utils  # optional helper for image upload (I show below)
import json

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/me", response_model=schemas.PatientOut)
def update_profile(
    dob: str | None = Form(None),
    gender: str | None = Form(None),
    medical_history: str | None = Form(None),  # comes in as string
    profile_image: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can update profile")

    patient = crud.get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    # ✅ Parse JSON string to Python list
    parsed_history = None
    if medical_history:
        try:
            parsed_history = json.loads(medical_history)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="medical_history must be valid JSON array")

    # ✅ Upload image if provided
    image_url = None
    if profile_image:
        image_url = cloudinary_utils.upload_file_to_cloudinary(profile_image)

    updated = crud.update_patient(
        db,
        current_user.id,
        dob=dob or patient.dob,
        gender=gender or patient.gender,
        medical_history=parsed_history or patient.medical_history,
        profile_image=image_url or patient.profile_image
    )
    return updated


# Get my patient profile
@router.get("/me", response_model=schemas.PatientOut)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients")
    patient = crud.get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient
