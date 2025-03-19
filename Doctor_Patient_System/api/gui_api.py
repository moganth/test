from fastapi import APIRouter, HTTPException
import sqlite3
from Doctor_Patient_System.config.constants import DATABASE_FILE, DATABASE_FILE1  # Import both DB files

router = APIRouter()

@router.get("/reports/patient_counts")
def get_patient_report_counts():
    try:
        conn_patients = sqlite3.connect(DATABASE_FILE)
        cursor_patients = conn_patients.cursor()

        conn_reports = sqlite3.connect(DATABASE_FILE1)
        cursor_reports = conn_reports.cursor()

        cursor_patients.execute("SELECT id, name FROM patients")
        patients_data = cursor_patients.fetchall()

        cursor_reports.execute("SELECT patient_id, COUNT(id) FROM reports GROUP BY patient_id")
        reports_data = dict(cursor_reports.fetchall())

        conn_patients.close()
        conn_reports.close()

        result = []
        for patient_id, name in patients_data:
            report_count = reports_data.get(patient_id, 0)
            result.append({"name": name, "report_count": report_count})

        if not result:
            raise HTTPException(status_code=404, detail="No data found")

        return result

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")