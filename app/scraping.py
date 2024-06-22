import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
import sys
sys.path.append(d)

import boto3
import fitz
from fastapi.responses import JSONResponse

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_REGION_NAME')
)

# class DataScraped:
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value

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

# from datetime import datetime
# def text_processing(text):
#     dataScraped = [
#         DataScraped('ast', '14g/dL'),
#         DataScraped('alt', '40mg/dL'),
#         DataScraped('creatinine', '1.2mg/dL'),
#     ]
#     randomDate = datetime(2024, 1, 30, 20, 50, 44, 296396)
#     return dataScraped, randomDate
from main import text_processing

def data_scraping(user_id: int, filename: str):
    text = extract_text_from_s3_pdf(user_id, filename)
    dataScraped, dateScraped = text_processing(text)
    return dataScraped, dateScraped
