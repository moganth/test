from datetime import datetime
import re
from database import Database
from student import Student
from teacher import Teacher

if __name__ == "__main__":
    student_db = Database("students.db")
    attendance_db = Database("attendance.db")
    student_manager = Student(attendance_db, student_db)
    teacher_manager = Teacher(attendance_db, student_db)

    while True:
        print("\nWelcome to the Student Attendance System")
        role = input("Are you a (1) Teacher or (2) Student or (3) Exit ? Enter 1 or 2 or 3: ")

        if role == "1":
            while True:
                print("\nTeacher Menu")
                print("1. Add Student")
                print("2. View Attendance")
                print("3. Edit Attendance")
                print("4. Download Attendance Report")
                print("5. Exit")
                choice = input("Enter choice: ")

                if choice == "1":
                    while True:
                        stu_id = input("Enter student ID: ")
                        if not stu_id.isdigit():
                            print("Error: Student ID must be Numeric. Try again!")
                            continue
                        break

                    while True:
                        name = input("Enter student name: ")
                        if not re.match(r"^[A-Za-z\s]+$", name):
                            print("Error: Name should only contain Letters. Try again!")
                            continue
                        break

                    while True:
                        roll_number = input("Enter roll number: ")
                        if not roll_number.isdigit():
                            print("Error: Roll number must be Numeric. Try again!")
                            continue
                        break

                    while True:
                        dob = input("Enter date of birth (YYYY-MM-DD): ")
                        try:
                            datetime.strptime(dob, "%Y-%m-%d")
                            break
                        except ValueError:
                            print("Error: Invalid Date of Birth format. Try again!")
                    teacher_manager.add_student(stu_id, name, roll_number, dob)
                elif choice == "2":
                    attendance = teacher_manager.view_attendance()
                    print("\nAttendance Records:")
                    for record in attendance:
                        print(f"ID: {record[3]}, Name: {record[0]}, Date: {record[1]}, Status: {record[2]}")
                elif choice == "3":
                    Student_id = input("Enter Student ID to edit: ")
                    new_status = input("Enter new status (Present/Absent): ")
                    if new_status in ["Present", "Absent"]:
                        teacher_manager.edit_attendance(Student_id, new_status)
                    else:
                        print("Invalid status. Enter 'Present' or 'Absent'.")
                elif choice == "4":
                    filename = input(
                        "Enter filename for the report: ")
                    teacher_manager.download_attendance(filename)
                elif choice == "5":
                    break
                else:
                    print("Invalid choice! Please enter 1, 2, 3, 4, or 5.")

        elif role == "2":
            student_id = input("Enter your student ID: ")
            while True:
                print("\nStudent Menu")
                print("1. Mark Attendance")
                print("2. Exit")
                choice = input("Enter choice: ")

                if choice == "1":
                    status = input("Enter status (Present/Absent): ")
                    if status in ["Present", "Absent"]:
                        student_manager.mark_attendance(student_id, status)
                    else:
                        print("Invalid status. Enter 'Present' or 'Absent'.")
                elif choice == "2":
                    break
                else:
                    print("Invalid choice! Please enter 1 or 2.")
        elif role == "3":
            break
        else:
            print("Invalid selection. Please enter 1 for Teacher or 2 for Student or 3 to Exit.")

    student_db.close_connection()
    attendance_db.close_connection()