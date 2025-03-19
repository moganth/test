import json
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
import sqlite3
from fastapi.responses import FileResponse
import requests

from Doctor_Patient_System.utils.logger import logger
from Hospital_Service.Patient_Service.config.constants import DATABASE_FILE, TEST_DIR, MQTT_TOPIC_TEST_SUBMISSION
from Hospital_Service.Patient_Service.models.patient_models import PatientBase
from Hospital_Service.Patient_Service.services.patient_service import PatientService
from Hospital_Service.Patient_Service.handlers.mqtt_handler import mqtt_client
from Hospital_Service.Patient_Service.database import get_db_connection

router = APIRouter()

os.makedirs(TEST_DIR, exist_ok=True)


@router.post("/patient/add_patient")
def add_patient(patient: PatientBase):
    return PatientService.add_patient(patient)


@router.get("/patient/get_patient/{patient_id}")
def get_patient(patient_id: int):
    try:
        patient = PatientService.get_patient(patient_id)
        if patient:
            return patient
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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


@router.get("/patient/get_reports/{patient_id}")
def get_reports(patient_id: int):
    try:
        response = requests.get(f"http://127.0.0.1:12398/doctor/get_reports/{patient_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="No reports found for this patient")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching reports")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Communication error with Doctor Service: {str(e)}")


@router.get("/patient/get_prescriptions/{patient_id}")
def get_prescriptions(patient_id: int):
    try:
        response = requests.get(f"http://127.0.0.1:12398/doctor/get_prescriptions/{patient_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="No prescriptions found for this patient")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching prescriptions")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Communication error with Doctor Service: {str(e)}")


@router.get("/patient/download_prescriptions/{patient_id}")
def download_prescriptions(patient_id: int):
    try:
        response = requests.get(f"http://127.0.0.1:12398/doctor/download_prescriptions/{patient_id}", stream=True)
        if response.status_code == 200:
            excel_path = f"prescriptions_patient_{patient_id}.xlsx"
            with open(excel_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return FileResponse(excel_path, filename=f"prescriptions_{patient_id}.xlsx",
                                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Unknown error"))
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Communication error with Doctor Service: {str(e)}")


@router.post("/patient/submit_test/")
def submit_test(report_id: int, test_file: UploadFile = File(...)):
    file_path = os.path.join(TEST_DIR, f"test_details_{report_id}.txt")
    with open(file_path, "wb") as f:
        f.write(test_file.file.read())

    mqtt_client.publish(MQTT_TOPIC_TEST_SUBMISSION, json.dumps({
        "report_id": report_id,
        "file_path": file_path
    }))

    return {"message": "Test submitted successfully", "file_path": file_path}