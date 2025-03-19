from fastapi import APIRouter, Depends
from Student_Attendance_System.services.teacher_service import TeacherService

router = APIRouter()

tservice = TeacherService()

@router.post("/add_student")
def add_student(stu_id: int, name: str, roll_number: str, dob: str):
    return tservice.add_student(stu_id, name, roll_number, dob)

@router.get("/view_attendance")
def view_attendance():
    return tservice.view_attendance()

@router.put("/edit_attendance")
def edit_attendance(stu_id: int, new_status: str):
    return tservice.edit_attendance(stu_id, new_status)

@router.get("/download_attendance")
def download_attendance():
    return tservice.download_attendance()
