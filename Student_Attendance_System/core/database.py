import sqlite3

def get_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    return conn, cursor

def init_db():
    conn, cursor = get_db()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        stu_id INTEGER PRIMARY KEY,
        name TEXT,
        roll_number TEXT,
        dob TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stu_id INTEGER,
        name TEXT,
        date TEXT,
        status TEXT,
        FOREIGN KEY(stu_id) REFERENCES students(stu_id)
    )""")
    conn.commit()
    conn.close()
