# modules/infections/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from modules.core.db import get_db
from modules.auth.security import get_current_user
from modules.users.models import User
from modules.patients import crud as patient_crud
from modules.infections import crud, schemas
from modules.core import cloudinary_utils
from modules.appointments import crud as appt_crud

router = APIRouter(prefix="/infections", tags=["infections"])

# helper: dummy AI call - replace with real integration
def call_ai_model_on_image_bytes(image_bytes: bytes):
    # Dummy: return a sample response. Replace with real API call:
    return {
        "diagnosis": "Possible fungal infection",
        "confidence": 0.86,
        "advice": "Apply anti-fungal cream twice daily for 2 weeks. Consult a dermatologist if it persists."
    }

@router.post("/diagnose", response_model=schemas.DiagnoseResponse)
def diagnose_infection(image: UploadFile = File(...), notes: str | None = Form(None), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can use diagnose feature")
    patient = patient_crud.get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")

    # upload image to Cloudinary (or local)
    image_url = cloudinary_utils.upload_file_to_cloudinary(image)

    # read bytes and send to AI
    contents = image.file.read()
    ai_resp = call_ai_model_on_image_bytes(contents)

    # decide if we recommend consultation (simple rule: confidence < threshold OR serious tags)
    recommend = ai_resp.get("confidence", 1.0) < 0.9  # example heuristic
    record = crud.create_infection_record(db, patient.id, image_url, ai_response=ai_resp, diagnosis=ai_resp.get("diagnosis"), confidence=ai_resp.get("confidence"), recommended_consultation=recommend)

    return {
        "id": record.id,
        "diagnosis": record.diagnosis,
        "confidence": record.confidence,
        "ai_response": str(ai_resp),
        "recommended_consultation": record.recommended_consultation
    }

# If patient wants consultation for a given infection record
@router.post("/{record_id}/consult", response_model=schemas.DiagnoseResponse)
def request_consult(record_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients")
    record = crud.get_infection_by_id(db, record_id)
    if not record or record.patient.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Record not found or not yours")

    # Try booking appointment (no specialization filter here, or set based on diagnosis)
    appt = appt_crud.book_earliest_slot_across_doctors(db, record.patient_id, preferred_specialization=None)
    if not appt:
        raise HTTPException(status_code=404, detail="No available slots to book")
    # Optionally update record to link appointment (not modeled)
    return {
        "id": record.id,
        "diagnosis": record.diagnosis,
        "confidence": record.confidence,
        "ai_response": record.ai_response,
        "recommended_consultation": True
    }
