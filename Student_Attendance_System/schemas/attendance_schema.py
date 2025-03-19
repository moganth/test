from pydantic import BaseModel

class AttendanceSchema(BaseModel):
    stu_id: int
    date: str
    status: str
