import os
import boto3
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