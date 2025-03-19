import csv
from database import Database

class Teacher:
    def __init__(self, attendance_db: Database, student_db: Database):
        self.attendance_db = attendance_db
        self.student_db = student_db

    def add_student(self, stu_id, name, roll_number, dob):
        try:
            self.student_db.cursor.execute(
                "INSERT INTO students (stu_id, name, roll_number, dob) VALUES (?, ?, ?, ?)",
                (stu_id, name, roll_number, dob)
            )
            self.student_db.conn.commit()
            print(f"Student '{name}' added successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def view_attendance(self):
        self.attendance_db.cursor.execute("SELECT id, stu_id, name, date, status FROM attendance")
        attendance_records = self.attendance_db.cursor.fetchall()

        final_records = []
        for record in attendance_records:
            attendance_id, stu_id, name, date, status = record
            final_records.append((name, date, status, stu_id))

        return final_records

    def edit_attendance(self, stu_id, new_status):
        self.attendance_db.cursor.execute("UPDATE attendance SET status = ? WHERE stu_id = ?", (new_status, stu_id))
        self.attendance_db.conn.commit()
        print(f"Attendance record {stu_id} updated to {new_status}")

    def download_attendance(self, filename="attendance_report.csv"):
        attendance_records = self.view_attendance()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name", "Date", "Status", "Student ID"])
            writer.writerows(attendance_records)
        print(f"Attendance report downloaded as {filename}")