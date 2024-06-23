from pydantic import BaseModel
from typing import Optional

class FormRequest(BaseModel):
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
    form_status: Optional[str]
    latest_red_blood_cell: Optional[float] 
    latest_hemoglobin: Optional[float] 
    latest_hematocrit: Optional[float] 
    latest_glycated_hemoglobin: Optional[float] 
    latest_ast: Optional[float] 
    latest_alt: Optional[float] 
    latest_urea: Optional[float] 
    latest_creatinine: Optional[float]