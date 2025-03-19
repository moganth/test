from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    email: Optional[EmailStr] = None
    contact: str
    address: str
    weight: float
    height: float
    past_health_records: Optional[str] = None
    created_at: datetime.datetime

class ReportBase(BaseModel):
    patient_id: int
    test_name: str
    disease: str
    created_at: datetime.datetime

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    prescription_details: str
    created_at: datetime.datetime

class TestRequest(BaseModel):
    patient_id: int
    doctor_id: int
    test_type: str
    test_details: str
    date: str

class TestSubmission(BaseModel):
    report_id: int
    test_details: str

class TestResult(BaseModel):
    report_id: int
    result: str
