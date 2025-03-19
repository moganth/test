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

class TestSubmission(BaseModel):
    report_id: int
    test_details: str