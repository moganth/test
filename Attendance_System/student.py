from datetime import date
from database import Database

class Student:
    def __init__(self, attendance_db: Database, student_db: Database):
        self.attendance_db = attendance_db
        self.student_db = student_db

    def get_students(self):
        self.student_db.cursor.execute("SELECT * FROM students")
        return self.student_db.cursor.fetchall()

    def mark_attendance(self, stu_id, status):
        today = date.today().strftime("%Y-%m-%d")

        self.student_db.cursor.execute("SELECT name FROM students WHERE stu_id = ?", (stu_id,))
        student = self.student_db.cursor.fetchone()

        if student:
            name = student[0]
            self.attendance_db.cursor.execute(
                "INSERT INTO attendance (stu_id, name, date, status) VALUES (?, ?, ?, ?)",
                (stu_id, name, today, status)
            )
            self.attendance_db.conn.commit()
            print(f"Attendance recorded for {name}: {status} on {today}")
        else:
            print("Error: Student ID not found!")
