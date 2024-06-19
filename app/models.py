from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, TIMESTAMP, CheckConstraint, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    biological_sex = Column(String(1), CheckConstraint("biological_sex IN ('M', 'F')"))
    creation_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    doctors = relationship("Doctor", back_populates="user")
    dependents = relationship("Dependent", back_populates="user", foreign_keys='Dependent.user_id')
    forms = relationship("Form", back_populates="user")
    tests = relationship("Test", back_populates="user")

class Doctor(Base):
    __tablename__ = 'doctors'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    crm = Column(String(50), nullable=False)
    specialty = Column(String(255), nullable=False)

    user = relationship("User", back_populates="doctors")

class Dependent(Base):
    __tablename__ = 'dependents'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    dependent_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    confirmed = Column(Boolean, default=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="dependents")
    dependent = relationship("User", foreign_keys=[dependent_id])

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    test_name = Column(String(255), nullable=False)
    url = Column(String(400), nullable=False)
    test_date = Column(TIMESTAMP, nullable=True, default=None)
    submission_date = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="tests")

class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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

    user = relationship("User", back_populates="forms")

    def to_dict(self):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "weight": self.weight,
                "height": self.height,
                "bmi": self.bmi,
                "blood_type": self.blood_type,
                "abdominal_circumference": self.abdominal_circumference,
                "allergies": self.allergies,
                "diseases": self.diseases,
                "medications": self.medications,
                "family_history": self.family_history,
                "important_notes": self.important_notes,
                "images_reports": self.images_reports,
                "form_status": self.form_status,
            }

class DerivedHealthData(Base):
    __tablename__ = 'derivedhealthdata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(Integer, ForeignKey('forms.id'), nullable=False)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    form = relationship("Form")
    test = relationship("Test")