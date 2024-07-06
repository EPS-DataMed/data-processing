from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, Form

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
import json
from datetime import datetime

def test_form_update_user_does_not_exist():
    user_id = 1
    
    form_data = {
        "weight": 70,
        "height": 175,
        "bmi": 22.9,
        "blood_type": "O+",
        "abdominal_circumference": 85,
        "allergies": "None",
        "diseases": "None",
        "medications": "None",
        "family_history": "None",
        "important_notes": "None",
        "images_reports": "None"
    }
    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["message"] == f"User with ID {user_id} not found"

def test_form_update_empty_form():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )
        db.add(user)
        db.commit()
    
    form_data = {}
    
    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 400
    assert response.json()["status"] == 400
    assert response.json()["message"] == "Empty form"

def test_partial_form_update():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )
        db.add(user)
        db.commit()
    
    form_data = {
        "weight": 70,
        "height": 175,
        "bmi": 22.9,
        "blood_type": "O+",
        "abdominal_circumference": 85,
        "allergies": "None",
        "diseases": "None",
        "medications": "None",
        "family_history": "None",
        "important_notes": "None",
        "images_reports": "None"
    }
    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"


def test_form_update_all_fields():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )
        db.add(user)
        db.commit()
    
    form_data = {
        "weight": 70,
        "height": 175,
        "bmi": 22.9,
        "blood_type": "O+",
        "abdominal_circumference": 85,
        "allergies": "Pollen",
        "diseases": "Hypertension",
        "medications": "Losartan",
        "family_history": "Family history of diabetes",
        "important_notes": "Non-smoker",
        "images_reports": "None",
        "latest_red_blood_cell": 5.1,
        "latest_hemoglobin": 14.5,
        "latest_hematocrit": 42.0,
        "latest_glycated_hemoglobin": 5.6,
        "latest_ast": 22,
        "latest_alt": 25,
        "latest_urea": 40,
        "latest_creatinine": 1.1
    }
    
    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"

def test_update_existing_form():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )

        form = Form(
            user_id = user_id,
            weight = 70,
            height = 175,
            bmi = 22.9,
            blood_type = "O+",
            abdominal_circumference = 85,
            allergies = "Pollen",
            diseases = "Hypertension",
            medications = "Losartan",
            family_history = "Family history of diabetes",
            important_notes = "Non-smoker",
            images_reports = "None",
            latest_red_blood_cell = 5.1,
            latest_hemoglobin = 14.5,
            latest_hematocrit = 42.0,
            latest_glycated_hemoglobin = 5.6,
            latest_ast = 22,
            latest_alt = 25,
            latest_urea = 40,
            latest_creatinine = 1.1
        )

        db.add(user)
        db.add(form)
        db.commit()

        form_data = {
            "weight": 70,
            "height": 175,
            "bmi": 22.9,
            "blood_type": "O+",
            "abdominal_circumference": 85,
            "allergies": "None",
            "diseases": "None",
            "medications": "None",
            "family_history": "None",
            "important_notes": "None",
            "images_reports": "None"
        }

    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"

def test_get_form():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )

        form = Form(
            user_id = user_id,
            weight = 70,
            height = 175,
            bmi = 22.9,
            blood_type = "O+",
            abdominal_circumference = 85,
            allergies = "Pollen",
            diseases = "Hypertension",
            medications = "Losartan",
            family_history = "Family history of diabetes",
            important_notes = "Non-smoker",
            images_reports = "None",
            form_status = "Filled",
            latest_red_blood_cell = 5.1,
            latest_hemoglobin = 14.5,
            latest_hematocrit = 42.0,
            latest_glycated_hemoglobin = 5.6,
            latest_ast = 22,
            latest_alt = 25,
            latest_urea = 40,
            latest_creatinine = 1.1
        )

        db.add(user)
        db.add(form)
        db.commit()

    response = client.get(f"/data/form-and-latest-tests/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The following form was found for user with ID '{user_id}'"


    data_from_response = response.json()["data"]

    expected_form_data = {
        "name": "Test User",
        "age": 24,
        "weight": "70",
        "height": "175",
        "bmi": "22.9",
        "blood_type": "O+",
        "abdominal_circumference": "85",
        "allergies": "Pollen",
        "diseases": "Hypertension",
        "medications": "Losartan",
        "family_history": "Family history of diabetes",
        "important_notes": "Non-smoker",
        "images_reports": "None",
        "form_status": "Filled",
        "latest_red_blood_cell": "5.1",
        "latest_hemoglobin": "14.5",
        "latest_hematocrit": "42.0",
        "latest_glycated_hemoglobin": "5.6",
        "latest_ast": "22",
        "latest_alt": "25",
        "latest_urea": "40",
        "latest_creatinine": "1.1"
    }

    assert data_from_response == expected_form_data

def test_get_form_user_not_found():
    user_id = 1
    response = client.get(f"/data/form-and-latest-tests/{user_id}")
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["message"] == f"User with ID {user_id} not found"

def test_get_form_not_found():
    user_id = 1
    with TestingSessionLocal() as db:
        user = User(
            id=user_id,
            full_name="Test User",
            email="testuser@example.com",
            password="password",
            birth_date=date(2000, 1, 1),
            biological_sex="M"
        )

        db.add(user)
        db.commit()
    
    response = client.get(f"/data/form-and-latest-tests/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"No form was found for user with ID '{user_id}'"