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

@pytest.fixture
def test_user1():
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
    return user_id

@pytest.fixture
def test_form1_for_test_user1(test_user1):
    with TestingSessionLocal() as db:
        user_id = test_user1
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
            important_notes = "None",
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
        db.add(form)
        db.commit()

@pytest.fixture
def partial_form():
    partial_form_data = {
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
    return partial_form_data

@pytest.fixture
def full_form():
    full_form_data = {
        "weight": 70,
        "height": 175,
        "bmi": 22.9,
        "blood_type": "O+",
        "abdominal_circumference": 85,
        "allergies": "Pollen",
        "diseases": "Hypertension",
        "medications": "Losartan",
        "family_history": "Family history of diabetes",
        "important_notes": "None",
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
    return full_form_data

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the data processing API"}

def test_pdf_tests_processing_user_not_found():
    user_id = 1
    test_list = [1]
    response = client.post(f"/data/tests-processing/{user_id}", json=test_list)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["message"] == f"User with ID '{user_id}' not found"


def test_pdf_tests_processing_test_not_found(test_user1):
    user_id = test_user1
    test_list = [1]
    response = client.post(f"/data/tests-processing/{user_id}", json=test_list)
    assert response.status_code == 404
    assert response.json() == {"status": 404, "message": f"Test with ID '{test_list[0]}' not found"}


def test_form_update_user_does_not_exist(partial_form):
    user_id = 1
    partial_form_data = partial_form

    response = client.put(f"/data/form/{user_id}", json=partial_form_data)
    assert response.status_code == 404
    assert response.json()["status"] == 404
    assert response.json()["message"] == f"User with ID '{user_id}' not found"

def test_form_update_empty_form(test_user1):
    user_id = test_user1
    form_data = {}

    response = client.put(f"/data/form/{user_id}", json=form_data)
    assert response.status_code == 400
    assert response.json()["status"] == 400
    assert response.json()["message"] == "Empty form"

def test_partial_form_update(test_user1, partial_form):
    user_id = test_user1
    
    partial_form_data = partial_form
    response = client.put(f"/data/form/{user_id}", json=partial_form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"


def test_form_update_all_fields(test_user1, full_form):
    user_id = test_user1    
    full_form_data = full_form

    response = client.put(f"/data/form/{user_id}", json=full_form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"

def test_update_existing_form(test_user1, test_form1_for_test_user1, partial_form):
    user_id = test_user1
    partial_form_data = partial_form

    response = client.put(f"/data/form/{user_id}", json=partial_form_data)
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The form was updated for user with ID '{user_id}'"

def test_get_form(test_user1, test_form1_for_test_user1):
    user_id = test_user1

    response = client.get(f"/data/form-and-latest-tests/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"The following form was found for user with ID '{user_id}'"


    data_from_response = response.json()["data"]

    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        birth_date = user.birth_date
        today = date.today()
        user_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    expected_form_data = {
        "name": "Test User",
        "age": user_age,
        "weight": "70",
        "height": "175",
        "bmi": "22.9",
        "blood_type": "O+",
        "abdominal_circumference": "85",
        "allergies": "Pollen",
        "diseases": "Hypertension",
        "medications": "Losartan",
        "family_history": "Family history of diabetes",
        "important_notes": "None",
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

def test_get_form_not_found(test_user1):
    user_id = test_user1
    
    response = client.get(f"/data/form-and-latest-tests/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["message"] == f"No form was found for user with ID '{user_id}'"