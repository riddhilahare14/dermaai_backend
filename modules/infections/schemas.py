# modules/infections/schemas.py
from pydantic import BaseModel
from typing import Optional

class DiagnoseResponse(BaseModel):
    id: int
    diagnosis: Optional[str]
    confidence: Optional[float]
    ai_response: Optional[str]
    recommended_consultation: bool

    model_config = {"from_attributes": True}

