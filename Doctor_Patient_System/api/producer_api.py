import json
import os
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
import sqlite3
from starlette.responses import FileResponse
import paho.mqtt.client as mqtt

from Doctor_Patient_System.config.constants import DATABASE_FILE, DATABASE_FILE1
from Doctor_Patient_System.models.base_model import PatientBase
from Doctor_Patient_System.config.constants import TEST, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_TEST_SUBMISSION

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

router = APIRouter()

os.makedirs(TEST, exist_ok=True)

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.post("/patient/add_patient")
def add_patient(patient: PatientBase):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO patients (name, age, gender, email, contact, address, weight, height, past_health_records, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient.name, patient.age, patient.gender, patient.email, patient.contact, patient.address,
              patient.weight, patient.height, patient.past_health_records, patient.created_at))
        conn.commit()
        return {"message": "Patient added successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


@router.put("/patient/update_patient/{patient_id}")
def update_patient(patient_id: int, patient: PatientBase):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE patients
            SET name = ?, age = ?, gender = ?, email = ?, contact = ?, address = ?, 
                weight = ?, height = ?, past_health_records = ?, created_at = ?
            WHERE id = ?
        ''', (patient.name, patient.age, patient.gender, patient.email, patient.contact, patient.address,
              patient.weight, patient.height, patient.past_health_records, patient.created_at, patient_id))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")

        conn.commit()
        return {"message": "Patient updated successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.delete("/patient/delete_patient/{patient_id}")
def delete_patient(patient_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")

        conn.commit()
        return {"message": "Patient deleted successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

def get_db_connection1():
    try:
        conn = sqlite3.connect(DATABASE_FILE1)
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.get("/patient/get_reports/{patient_id}")
def get_reports(patient_id: int):
    try:
        conn = sqlite3.connect(DATABASE_FILE1)
        cursor = conn.cursor()
        cursor.execute("SELECT id, patient_id, doctor_id, test_type, test_details, date FROM reports WHERE patient_id=?",
                       (patient_id,))
        reports = cursor.fetchall()
        conn.close()

        if not reports:
            raise HTTPException(status_code=404, detail="No reports found for this patient")

        df = pd.DataFrame(reports, columns=["ID", "Patient ID", "doctor_id", "test_type", "test_details", "date"])
        file_path = f"patient_{patient_id}_reports.xlsx"
        df.to_excel(file_path, index=False)

        return FileResponse(file_path, filename=file_path,
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except sqlite3.Error as db_error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/patient/submit_test/")
def submit_test(report_id: int, test_file: UploadFile = File(...)):
    file_path = os.path.join(TEST, f"test_details_{report_id}.txt")
    with open(file_path, "wb") as f:
        f.write(test_file.file.read())

    mqtt_client.publish(MQTT_TOPIC_TEST_SUBMISSION, json.dumps({
        "report_id": report_id,
        "file_path": file_path
    }))

    return {"message": "Test submitted successfully", "file_path": file_path}

