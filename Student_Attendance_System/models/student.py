from pydantic import BaseModel

class Student(BaseModel):
    stu_id: int
    name: str
    roll_number: str
    dob: str