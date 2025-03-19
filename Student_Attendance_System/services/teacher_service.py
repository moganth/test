import csv

from Student_Attendance_System.core.database import get_db


class TeacherService:
    def add_student(self, stu_id: int, name: str, roll_number: str, dob: str):
        conn, cursor = get_db()
        cursor.execute("INSERT INTO students (stu_id, name, roll_number, dob) VALUES (?, ?, ?, ?)", (stu_id, name, roll_number, dob))
        conn.commit()
        conn.close()
        return {"message": f"Student {name} added successfully!"}

    def view_attendance(self):
        conn, cursor = get_db()
        cursor.execute("SELECT stu_id, name, date, status FROM attendance")
        records = cursor.fetchall()
        conn.close()
        return records

    def edit_attendance(self, stu_id: int, new_status: str):
        conn, cursor = get_db()
        cursor.execute("UPDATE attendance SET status = ? WHERE stu_id = ?", (new_status, stu_id))
        conn.commit()
        conn.close()
        return {"message": f"Attendance record updated to {new_status}"}

    def download_attendance(self):
        conn, cursor = get_db()
        cursor.execute("SELECT name, date, status, stu_id FROM attendance")
        records = cursor.fetchall()
        conn.close()
        with open("attendance_report.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Date", "Status", "Student ID"])
            writer.writerows(records)
        return {"message": "Attendance report downloaded as attendance_report.csv"}