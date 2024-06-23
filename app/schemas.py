from pydantic import BaseModel, Field
from typing import Optional

class FormRequest(BaseModel):
    weight: Optional[float] = Field(None, alias="weight")
    height: Optional[float] = Field(None, alias="height")
    bmi: Optional[float] = Field(None, alias="bmi")
    blood_type: Optional[str] = Field(None, alias="blood_type")
    abdominal_circumference: Optional[float] = Field(None, alias="abdominal_circumference")
    allergies: Optional[str] = Field(None, alias="allergies")
    diseases: Optional[str] = Field(None, alias="diseases")
    medications: Optional[str] = Field(None, alias="medications")
    family_history: Optional[str] = Field(None, alias="family_history")
    important_notes: Optional[str] = Field(None, alias="important_notes")
    images_reports: Optional[str] = Field(None, alias="images_reports")
    form_status: Optional[str] = Field(None, alias="form_status")
    latest_red_blood_cell: Optional[float] = Field(None, alias="latest_red_blood_cell")
    latest_hemoglobin: Optional[float] = Field(None, alias="latest_hemoglobin")
    latest_hematocrit: Optional[float] = Field(None, alias="latest_hematocrit")
    latest_glycated_hemoglobin: Optional[float] = Field(None, alias="latest_glycated_hemoglobin")
    latest_ast: Optional[float] = Field(None, alias="latest_ast")
    latest_alt: Optional[float] = Field(None, alias="latest_alt")
    latest_urea: Optional[float] = Field(None, alias="latest_urea")
    latest_creatinine: Optional[float] = Field(None, alias="latest_creatinine")

    class Config:
        allow_population_by_field_name = True
