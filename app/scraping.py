import os
import re
import fitz
from datetime import datetime
from utils import s3_client
from fastapi.responses import JSONResponse

class DataScraped:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def extract_text_from_s3_pdf(user_id: int, filename: str) -> str:
    s3_key = f"{user_id}/{filename}"

    try:
        response = s3_client.get_object(
            Bucket=os.getenv('S3_BUCKET_NAME'),
            Key=s3_key
        )
        pdf_data = response['Body'].read()
        doc = fitz.open(stream=pdf_data, filetype='pdf')
        
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()

        doc.close()

        return text
    except Exception as e:
        return JSONResponse(content={"status": 500, "message": f"Error while downloading the file '{filename}' on AWS S3 for user '{user_id}'"}, status_code=500)
    
def extract_values_from_text(text, patterns):
    results = []
    for key, (pattern, unit) in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            name = key
            # value = f"{match.group(1)} {unit}"
            value = f"{match.group(1)}"
            value = value.replace(',', '.')
            results.append(
                DataScraped(name, value)
            )
    return results

def extract_test_date(text):
    pattern_date = r'Atendimento\s*:\s*(\d{2}/\d{2}/\d{4})'
    match = re.search(pattern_date, text)
    if match:
        return datetime.strptime(match.group(1), '%d/%m/%Y')
    return None

def extract_data_and_date(text):
    patterns = {
        "hemoglobin": (r'HEMOGLOBINA\s*([\d,\.]+)\s*g/dL', "g/dL"),
        "hematocrit": (r'HEMATÓCRITO\s*([\d,\.]+)\s*%', "%"),
        "red_blood_cell": (r'HEMÁCIAS\s*([\d,\.]+)\s*milhões/mm3', "milhões/mm3"),
        "glycated_hemoglobin": (r'HEMOGLOBINA GLICADA - HbA1c\s*.*?RESULTADO:\s*([\d,\.]+)\s*%', "%"),
        "ast": (r'TRANSAMINASE OXALACÉTICA TGO \(AST\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "alt": (r'TRANSAMINASE PIRÚVICA TGP \(ALT\).*?RESULTADO:\s*([\d,\.]+)\s*U/L', "U/L"),
        "urea": (r'UREIA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL"),
        "creatinine": (r'CREATININA\s*.*?RESULTADO:\s*([\d,\.]+)\s*mg/dL', "mg/dL")
    }
    
    test_date = extract_test_date(text)
    
    data_values = extract_values_from_text(text, patterns)
    
    return data_values, test_date

def text_processing(text):
    data_values, test_date = extract_data_and_date(text)
    return data_values, test_date

def data_scraping(user_id: int, filename: str):
    text = extract_text_from_s3_pdf(user_id, filename)
    dataScraped, dateScraped = text_processing(text)
    return dataScraped, dateScraped
