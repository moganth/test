from Student_Attendance_System.core.database import get_db
from datetime import datetime

class StudentService:
    def get_student_profile(self, stu_id: int):
        conn, cursor = get_db()
        cursor.execute("SELECT * FROM students WHERE stu_id = ?", (stu_id,))
        student = cursor.fetchone()
        conn.close()
        if student:
            return {"stu_id": student[0], "name": student[1], "roll_number": student[2], "dob": student[3]}
        return {"message": "Student not found"}

    def edit_own_attendance(self, stu_id: int, new_status: str):
        conn, cursor = get_db()
        today_date = datetime.today().strftime('%Y-%m-%d')

        cursor.execute("SELECT * FROM attendance WHERE stu_id = ? AND date = ?", (stu_id, today_date))
        existing_record = cursor.fetchone()

        if existing_record:
            cursor.execute("UPDATE attendance SET status = ? WHERE stu_id = ? AND date = ?",
                           (new_status, stu_id, today_date))
        else:
            cursor.execute("SELECT name FROM students WHERE stu_id = ?", (stu_id,))
            student = cursor.fetchone()
            if student:
                name = student[0]
                cursor.execute("INSERT INTO attendance (stu_id, name, date, status) VALUES (?, ?, ?, ?)",
                               (stu_id, name, today_date, new_status))
            else:
                conn.close()
                return {"message": "Student not found"}

        conn.commit()
        conn.close()
        return {"message": f"Your attendance for {today_date} has been updated to {new_status}"}
