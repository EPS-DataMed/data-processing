from pydantic import BaseModel
from typing import Optional

class Form(BaseModel):
    weight: Optional[float]
    height: Optional[float]
    bmi: Optional[float]
    blood_type: Optional[str]
    abdominal_circumference: Optional[float]
    allergies: Optional[str]
    diseases: Optional[str]
    medications: Optional[str]
    family_history: Optional[str]
    important_notes: Optional[str]
    images_reports: Optional[str]