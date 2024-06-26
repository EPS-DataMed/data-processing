import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User
from app.database import load_users_from_csv
import os
import csv

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_load_users_from_csv():
    test_csv = "test_users.csv"
    with open(test_csv, 'w', newline='') as csvfile:
        fieldnames = ['name', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'name': 'Luiz Gustavo', 'email': 'luiz.gustavo@example.com'})
        writer.writerow({'name': 'Maria Silva', 'email': 'maria.silva@example.com'})
    
    db = TestingSessionLocal()
    load_users_from_csv(db, test_csv)
    users = db.query(User).all()
    assert len(users) == 2
    assert users[0].name == 'Luiz Gustavo'
    assert users[0].email == 'luiz.gustavo@example.com'
    assert users[1].name == 'Maria Silva'
    assert users[1].email == 'maria.silva@example.com'
    os.remove(test_csv)