from pydantic import BaseModel
import datetime

class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    prescription_details: str
    created_at: datetime.datetime

class ReportBase(BaseModel):
    patient_id: int
    test_name: str
    disease: str
    created_at: datetime.datetime

class TestRequest(BaseModel):
    patient_id: int
    doctor_id: int
    test_type: str
    test_details: str
    date: str

class TestResult(BaseModel):
    report_id: int
    result: str