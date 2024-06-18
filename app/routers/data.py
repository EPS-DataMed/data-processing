import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
import sys
sys.path.append(d)

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from datetime import datetime
import models
from schemas import Form
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def is_form_filled(form: Form) -> bool:
    form_fields = [
        form.weight,
        form.height,
        form.bmi,
        form.blood_type,
        form.abdominal_circumference,
        form.allergies,
        form.diseases,
        form.medications,
        form.family_history,
        form.important_notes,
        form.images_reports
    ]

    return all(field is not None for field in form_fields)

class DataScraped:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def data_scraping(test_id):
    dataScraped = [
        DataScraped('ast', '14g/dL'),
        DataScraped('alt', '40mg/dL'),
        DataScraped('creatinine', '1.2mg/dL'),
    ]
    randomDate = datetime(2024, 1, 30, 20, 50, 44, 296396)
    return dataScraped, randomDate

@app.get("/")
async def root():
    return {"message": "Data processing service"}

@app.post("/data/tests-processing/{user_id}")
async def tests_processing(user_id: int, testsIdList: List[int], db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": "User not found"}, status_code=404)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    if not user_form:
        user_form = models.Form(user_id=user_id)
        db.add(user_form)
        db.commit()
        db.refresh(user_form)

    for test_id in testsIdList:
        dataScraped, scrapeTime = data_scraping(test_id)
        test = db.query(models.Test).filter(models.Test.id == test_id).first()
        if not test:
            return JSONResponse(content={"status": 404, "message": f"Test with ID '{test_id}' not found"}, status_code=404)
        elif test.user_id != user_id:
            return JSONResponse(content={"status": 400, "message": f"Test with ID '{test_id}' is not a test of the user with ID {user_id}"}, status_code=400)
        else:
            test.test_date = scrapeTime
            db.add(test)

        for data in dataScraped:
            new_health_data = models.DerivedHealthData(
                form_id=user_form.id,
                test_id=test_id,
                name=data.name,
                value=data.value
            )
            db.add(new_health_data)    
    db.commit()
    
    latest_values = {}
    metrics = ['red_blood_cells', 'hemoglobin', 'hematocrit', 'glycated_hemoglobin', 'ast', 'alt', 'urea', 'creatinine']
    for metric in metrics:
        latest_value = (
            db.query(models.DerivedHealthData)
            .join(models.Test, models.DerivedHealthData.test_id == models.Test.id)
            .join(models.Form, models.DerivedHealthData.form_id == models.Form.id)
            .filter(
                models.DerivedHealthData.name == metric,
                models.Form.user_id == user_id
            )
            .order_by(models.Test.test_date.desc())
            .first()
        )
        latest_values[metric] = latest_value.value if latest_value else None

    return JSONResponse(content={"status": 200, "message": f"The following form was updated for user with ID '{user_id}'", "data": latest_values}, status_code=200)

@app.put("/data/form/{user_id}")
async def update_form(user_id: int, resquest_form: Form, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": "User not found"}, status_code=404)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    resquest_form_dict = resquest_form.dict(exclude_unset=True)
    
    if not user_form:
        form_status = "Filled" if is_form_filled(resquest_form) else "In progress"
        user_form = models.Form(user_id=user_id, form_status=form_status, **resquest_form_dict)
        db.add(user_form)
    else:
        for key, value in resquest_form_dict.items():
            setattr(user_form, key, value)
        form_status = "Filled" if is_form_filled(user_form) else "In progress"
        user_form.form_status = form_status
    db.commit()
    db.refresh(user_form)

    user_form_dict = user_form.to_dict()
    return JSONResponse(content={"status": 200, "message": f"The following form was updated for user with ID '{user_id}'", "data": user_form_dict}, status_code=200)

@app.get("/data/form-and-latest-tests/{user_id}")
async def get_form_and_latest_tests(user_id: int, db: Session = Depends(get_db)):

    form_response = []

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": "User not found"}, status_code=404)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    if not user_form:
        return JSONResponse(content={"status": 200, "message": f"No form was found for user with ID '{user_id}'", "data": form_response}, status_code=200)

    latest_values = {}
    metrics = ['red_blood_cells', 'hemoglobin', 'hematocrit', 'glycated_hemoglobin', 'ast', 'alt', 'urea', 'creatinine']
    for metric in metrics:
        latest_value = (
            db.query(models.DerivedHealthData)
            .join(models.Test, models.DerivedHealthData.test_id == models.Test.id)
            .join(models.Form, models.DerivedHealthData.form_id == models.Form.id)
            .filter(
                models.DerivedHealthData.name == metric,
                models.Form.user_id == user_id
            )
            .order_by(models.Test.test_date.desc())
            .first()
        )
        latest_values[metric] = latest_value.value if latest_value else None

    form_response = {
        "name": user.full_name,
        "age": (datetime.now().date() - user.birth_date).days // 365,
        "weight": user_form.weight,
        "height": user_form.height,
        "bmi": user_form.bmi,
        "blood_type": user_form.blood_type,
        "abdominal_circumference": user_form.abdominal_circumference,
        "red_blood_cells": latest_values.get('red_blood_cells'),
        "hemoglobin": latest_values.get('hemoglobin'),
        "hematocrit": latest_values.get('hematocrit'),
        "glycated_hemoglobin": latest_values.get('glycated_hemoglobin'),
        "ast": latest_values.get('ast'),
        "alt": latest_values.get('alt'),
        "urea": latest_values.get('urea'),
        "creatinine": latest_values.get('creatinine'),        
        "allergies": user_form.allergies,
        "diseases": user_form.diseases,
        "medications": user_form.medications,
        "family_history": user_form.family_history,
        "important_notes": user_form.important_notes,
        "images_reports": user_form.images_reports,
        "form_status": user_form.form_status
        }
    return JSONResponse(content={"status": 200, "message": f"The following form was found for user with ID '{user_id}'", "data": form_response}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(
        "data:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

