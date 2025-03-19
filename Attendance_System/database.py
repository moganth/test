import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        if self.db_name == "students.db":
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stu_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    roll_number TEXT UNIQUE NOT NULL,
                    dob TEXT NOT NULL
                )
            """)
        elif self.db_name == "attendance.db":
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stu_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    date TEXT,
                    status TEXT CHECK(status IN ('Present', 'Absent')),
                    FOREIGN KEY(stu_id) REFERENCES students(stu_id)
                )
            """)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
