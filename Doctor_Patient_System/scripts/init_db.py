import sqlite3

from Doctor_Patient_System.utils.logger import logger
from Doctor_Patient_System.config.constants import DATABASE_FILE,DATABASE_FILE1

def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (  id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL CHECK (age > 0),  -- Ensures age is positive
        gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),  -- Restrict to 'Male' or 'Female'
        email TEXT UNIQUE NOT NULL,
        contact TEXT NOT NULL CHECK (LENGTH(contact) = 10 AND contact GLOB '[0-9]*'), -- Ensures 10-digit numeric contact
        address TEXT NOT NULL,
        weight REAL NOT NULL CHECK (weight > 0),  -- Ensures weight is positive
        height REAL NOT NULL CHECK (height > 0),  -- Ensures height is positive
        past_health_records TEXT,
        created_at TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            test_name TEXT,
            disease TEXT,
            created_at TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                prescription_details TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        ''')

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully!")

def initialize_db_1():
    conn = sqlite3.connect(DATABASE_FILE1)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        test_type TEXT,
        test_details TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()
    logger.info("Database_1 initialized successfully!")

if __name__ == "__main__":
    initialize_db()
    initialize_db_1()
