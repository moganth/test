from pydantic import BaseModel

class Data(BaseModel):
    student_id: int
    dob: str
    date: str
    attendance: str

class Condition(BaseModel):
    alert: bool

class Message(BaseModel):
    data: Data
    condition: Condition
