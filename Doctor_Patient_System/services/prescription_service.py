import sqlite3
from Doctor_Patient_System.config.constants import DATABASE_FILE

class PrescriptionService:
    @staticmethod
    def add_prescription(prescription_data):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prescriptions (patient_id, doctor_id, prescription_details, created_at)
            VALUES (?, ?, ?, ?)
        ''', (
            prescription_data.patient_id, prescription_data.doctor_id,
            prescription_data.prescription_details, prescription_data.created_at
        ))
        conn.commit()
        conn.close()
        return {"message": "Prescription added successfully"}

    @staticmethod
    def get_prescriptions_by_patient(patient_id):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prescriptions WHERE patient_id=?", (patient_id,))
        prescriptions = cursor.fetchall()
        conn.close()
        if not prescriptions:
            return []
        return [dict(zip([column[0] for column in cursor.description], pres)) for pres in prescriptions]
