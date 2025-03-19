import sqlite3
from fastapi import HTTPException
from Hospital_Service.Patient_Service.config.constants import DATABASE_FILE
from Hospital_Service.Patient_Service.utils.logger import logger

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

def initialize_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK (age > 0),
            gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),
            email TEXT UNIQUE NOT NULL,
            contact TEXT NOT NULL CHECK (LENGTH(contact) = 10 AND contact GLOB '[0-9]*'),
            address TEXT NOT NULL,
            weight REAL NOT NULL CHECK (weight > 0),
            height REAL NOT NULL CHECK (height > 0),
            past_health_records TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("Patient Service database initialized successfully!")