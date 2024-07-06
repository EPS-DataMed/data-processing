import os
import boto3
from datetime import datetime
from app.schemas import FormRequest

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_REGION_NAME')
)

def is_form_filled(form: FormRequest) -> bool:
    required_form_fields = [
        form.weight,
        form.height,
        form.bmi,
        form.blood_type,
        form.abdominal_circumference,
        form.allergies,
        form.diseases,
        form.medications,
        form.family_history,
        form.form_status,
        form.latest_red_blood_cell, 
        form.latest_hemoglobin, 
        form.latest_hematocrit, 
        form.latest_glycated_hemoglobin, 
        form.latest_ast, 
        form.latest_alt, 
        form.latest_urea, 
        form.latest_creatinine
    ]

    return all(field is not None for field in required_form_fields)

def create_form_response(user, user_form):
    return {
        "name": user.full_name,
        "age": (datetime.now().date() - user.birth_date).days // 365,
        "weight": user_form.weight,
        "height": user_form.height,
        "bmi": user_form.bmi,
        "blood_type": user_form.blood_type,
        "abdominal_circumference": user_form.abdominal_circumference,
        "allergies": user_form.allergies,
        "diseases": user_form.diseases,
        "medications": user_form.medications,
        "family_history": user_form.family_history,
        "important_notes": user_form.important_notes,
        "images_reports": user_form.images_reports,
        "form_status": user_form.form_status,
        "latest_red_blood_cell": user_form.latest_red_blood_cell,
        "latest_hemoglobin": user_form.latest_hemoglobin,
        "latest_hematocrit": user_form.latest_hematocrit,
        "latest_glycated_hemoglobin": user_form.latest_glycated_hemoglobin,
        "latest_ast": user_form.latest_ast,
        "latest_alt": user_form.latest_alt,
        "latest_urea": user_form.latest_urea,
        "latest_creatinine": user_form.latest_creatinine
    }