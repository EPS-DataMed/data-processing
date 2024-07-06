from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from app import models
from app.database import get_db
from app.schemas import FormRequest
from app.scraping import data_scraping
from app.utils import is_form_filled, create_form_response

router = APIRouter(
    prefix="/data",
    tags=['Data']
)

@router.post("/tests-processing/{user_id}")
async def tests_processing(user_id: int, testsIdList: List[int], db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": f"User with ID '{user_id}' not found"}, status_code=404)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    if not user_form:
        user_form = models.Form(user_id=user_id)
        db.add(user_form)
        db.commit()
        db.refresh(user_form)

    for test_id in testsIdList:
        test = db.query(models.Test).filter(models.Test.id == test_id).first()
        if not test:
            return JSONResponse(content={"status": 404, "message": f"Test with ID '{test_id}' not found"}, status_code=404)
        elif test.user_id != user_id:
            return JSONResponse(content={"status": 400, "message": f"Test with ID '{test_id}' is not a test of the user with ID {user_id}"}, status_code=400)

        filename = test.test_name
        dataScraped, dateScraped = data_scraping(user_id, filename)
        test.test_date = dateScraped
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
    metrics = ['red_blood_cell', 'hemoglobin', 'hematocrit', 'glycated_hemoglobin', 'ast', 'alt', 'urea', 'creatinine']
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
        if latest_values.get(metric) is not None:
            setattr(user_form, f'latest_{metric}', latest_values.get(metric))

    if any(latest_values.values()):
        user_form.form_status = "In progress" if user_form.form_status != "Filled" else user_form.form_status
        db.commit()
        db.refresh(user_form)
    
    form_response = create_form_response(user, user_form)
    
    return JSONResponse(content={"status": 200, "message": f"The following form was updated for user with ID '{user_id}'", "data": form_response}, status_code=200)

@router.put("/form/{user_id}")
async def update_form(user_id: int, request_form: FormRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": f"User with ID '{user_id}' not found"}, status_code=404)

    if not request_form.dict(exclude_none=True):
        return JSONResponse(content={"status": 400, "message": "Empty form"}, status_code=400)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    request_form_dict = request_form.dict(exclude_unset=True)
    
    if not user_form:
        form_status = "Filled" if is_form_filled(request_form) else "In progress"
        user_form = models.Form(user_id=user_id, form_status=form_status, **request_form_dict)
        db.add(user_form)
    else:
        for key, value in request_form_dict.items():
            setattr(user_form, key, value)
        form_status = "Filled" if is_form_filled(user_form) else "In progress"
        user_form.form_status = form_status
    db.commit()
    db.refresh(user_form)

    return JSONResponse(content={"status": 200, "message": f"The form was updated for user with ID '{user_id}'"}, status_code=200)

@router.get("/form-and-latest-tests/{user_id}")
async def get_form(user_id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return JSONResponse(content={"status": 404, "message": f"User with ID {user_id} not found"}, status_code=404)

    user_form = db.query(models.Form).filter(models.Form.user_id == user_id).first()
    if not user_form:
        form_response = {}
        return JSONResponse(content={"status": 200, "message": f"No form was found for user with ID '{user_id}'", "data": form_response}, status_code=200)
    
    form_response = create_form_response(user, user_form)
    return JSONResponse(content={"status": 200, "message": f"The following form was found for user with ID '{user_id}'", "data": form_response}, status_code=200)