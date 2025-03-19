import json
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
import sqlite3
from fastapi.responses import FileResponse
import pandas as pd

from Doctor_Patient_System.api.producer_api import get_db_connection, get_db_connection1, mqtt_client
from Doctor_Patient_System.config.constants import DATABASE_FILE, DATABASE_FILE1, REPORT, MQTT_TOPIC_TEST_RESULT
from Doctor_Patient_System.models.base_model import PrescriptionBase, ReportBase, TestRequest
from Doctor_Patient_System.services.patient_service import PatientService
from Doctor_Patient_System.services.prescription_service import PrescriptionService
from Doctor_Patient_System.services.report_1_service import request_test

router = APIRouter()

os.makedirs(REPORT, exist_ok=True)

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

@router.post("/doctor/add_report")
def add_report(report: ReportBase):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reports (patient_id, test_name, disease, created_at)
            VALUES (?, ?, ?, ?)
        ''', (report.patient_id, report.test_name, report.disease, report.created_at))
        conn.commit()
        return {"message": "Report added successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

@router.get("/doctor/get_reports/{patient_id}")
def get_reports(patient_id: int):
    try:
        conn = sqlite3.connect(DATABASE_FILE1)
        cursor = conn.cursor()
        cursor.execute("SELECT id, patient_id, test_name, disease, created_at FROM reports WHERE patient_id=?",
                       (patient_id,))
        reports = cursor.fetchall()
        conn.close()

        if not reports:
            raise HTTPException(status_code=404, detail="No reports found for this patient")

        df = pd.DataFrame(reports, columns=["ID", "Patient ID", "Test Name", "Disease", "Created At"])
        file_path = f"patient_{patient_id}_reports.xlsx"
        df.to_excel(file_path, index=False)

        return FileResponse(file_path, filename=file_path,
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except sqlite3.Error as db_error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/doctor/add_prescription")
def add_prescription(prescription: PrescriptionBase):
    response = PrescriptionService.add_prescription(prescription)
    return response

@router.post("/doctor/request_test/")
def request_test_api(request: TestRequest):
    return request_test(request)

@router.post("/doctor/submit_result/")
def submit_result(report_id: int, result_file: UploadFile = File(...)):
    file_path = os.path.join(REPORT, f"result_{report_id}.txt")
    with open(file_path, "wb") as f:
        f.write(result_file.file.read())

    mqtt_client.publish(MQTT_TOPIC_TEST_RESULT, json.dumps({
        "report_id": report_id,
        "file_path": file_path
    }))
    return {"message": "Test requested", "report_id": report_id}
