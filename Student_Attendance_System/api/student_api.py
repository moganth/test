from fastapi import APIRouter, Depends
from Student_Attendance_System.services.student_service import StudentService

router = APIRouter()

sservice = StudentService()

@router.get("/profile")
def get_student_profile(stu_id: int):
    return sservice.get_student_profile(stu_id)

@router.put("/edit_attendance")
def edit_own_attendance(stu_id: int, new_status: str):
    return sservice.edit_own_attendance(stu_id, new_status)