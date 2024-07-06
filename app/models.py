from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, TIMESTAMP, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(2048), nullable=False)
    birth_date = Column(Date, nullable=False)
    biological_sex = Column(String(1), CheckConstraint("biological_sex IN ('M', 'F')"))
    creation_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    doctors = relationship("Doctor", back_populates="user")
    dependents = relationship("Dependent", back_populates="user", foreign_keys='Dependent.user_id')
    forms = relationship("Form", back_populates="user")
    tests = relationship("Test", back_populates="user")

class Doctor(Base):
    __tablename__ = 'Doctors'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    crm = Column(String(50), nullable=False)
    specialty = Column(String(255), nullable=False)

    user = relationship("User", back_populates="doctors")

class Dependent(Base):
    __tablename__ = 'Dependents'
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    dependent_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    confirmed = Column(Boolean, default=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="dependents")
    dependent = relationship("User", foreign_keys=[dependent_id])

class Test(Base):
    __tablename__ = 'Tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    test_name = Column(String(255), nullable=False)
    url = Column(String(400), nullable=False)
    test_date = Column(TIMESTAMP, nullable=True, default=None)
    submission_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="tests")

class Form(Base):
    __tablename__ = 'Forms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    weight = Column(String(255))
    height = Column(String(255))
    bmi = Column(String(255))
    blood_type = Column(String(255))
    abdominal_circumference = Column(String(255))
    allergies = Column(String(255))
    diseases = Column(String(255))
    medications = Column(String(255))
    family_history = Column(String(255))
    important_notes = Column(String(255))
    images_reports = Column(String(255))
    form_status = Column(String(20), CheckConstraint("form_status IN ('Filled', 'In progress', 'Not started')"), default='Not started')
    latest_red_blood_cell = Column(String(255))
    latest_hemoglobin = Column(String(255))
    latest_hematocrit = Column(String(255))
    latest_glycated_hemoglobin = Column(String(255))
    latest_ast = Column(String(255))
    latest_alt = Column(String(255))
    latest_urea = Column(String(255))
    latest_creatinine = Column(String(255))

    user = relationship("User", back_populates="forms")

class DerivedHealthData(Base):
    __tablename__ = 'DerivedHealthData'
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey('Forms.id'), nullable=False)
    test_id = Column(Integer, ForeignKey('Tests.id'), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    form = relationship("Form")
    test = relationship("Test")