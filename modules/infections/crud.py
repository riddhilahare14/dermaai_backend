# modules/infections/crud.py
from sqlalchemy.orm import Session
from modules.infections.models import InfectionRecord
import json

def create_infection_record(db: Session, patient_id: int, image_url: str, ai_response: dict | None = None, diagnosis: str | None = None, confidence: float | None = None, recommended_consultation: bool = False):
    record = InfectionRecord(
        patient_id=patient_id,
        image_url=image_url,
        ai_response=json.dumps(ai_response) if ai_response else None,
        diagnosis=diagnosis,
        confidence=confidence,
        recommended_consultation=recommended_consultation
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_infection_by_id(db: Session, record_id: int):
    return db.query(InfectionRecord).filter(InfectionRecord.id == record_id).first()
