import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import app.models as models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post("/users/", json={"name": "Luiz Gustavo", "email": "luiz.gustavo@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Luiz Gustavo"
    assert data["email"] == "luiz.gustavo@example.com"

def test_read_user():
    response = client.post("/users/", json={"name": "Luiz Gustavo", "email": "luiz.gustavo@example.com"})
    user_id = response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Luiz Gustavo"
    assert data["email"] == "luiz.gustavo@example.com"

def test_update_user():
    response = client.post("/users/", json={"name": "Luiz Gustavo", "email": "luiz.gustavo@example.com"})
    user_id = response.json()["id"]
    
    response = client.patch(f"/users/{user_id}", json={"name": "Gustavo Luiz"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Gustavo Luiz"

def test_delete_user():
    response = client.post("/users/", json={"name": "Luiz Gustavo", "email": "luiz.gustavo@example.com"})
    user_id = response.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] == True