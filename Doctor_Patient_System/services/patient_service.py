import sqlite3
from Doctor_Patient_System.config.constants import DATABASE_FILE

class PatientService:
    @staticmethod
    def add_patient(patient_data):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO patients (name, age, gender, email, contact, address, weight, height, past_health_records, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_data.name, patient_data.age, patient_data.gender, patient_data.email,
                patient_data.contact, patient_data.address, patient_data.weight,
                patient_data.height, patient_data.past_health_records, patient_data.created_at
            ))
            conn.commit()
            return {"message": "Patient added successfully"}
        except sqlite3.IntegrityError:
            return {"error": "Integrity constraint violated (e.g., duplicate email)"}
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}
        finally:
            conn.close()

    @staticmethod
    def get_patient(patient_id):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "age": row[2], "gender": row[3]}
            return {"error": "Patient not found"}
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}
        finally:
            conn.close()
