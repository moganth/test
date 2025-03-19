import json
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
import sqlite3
from fastapi.responses import FileResponse
import pandas as pd
import requests

from Hospital_Service.Doctor_Service.config.constants import DATABASE_FILE, REPORT_DIR, MQTT_TOPIC_TEST_RESULT
from Hospital_Service.Doctor_Service.models.doctor_models import PrescriptionBase, ReportBase, TestRequest
from Hospital_Service.Doctor_Service.services.prescription_service import PrescriptionService
from Hospital_Service.Doctor_Service.services.report_service import ReportService, request_test
from Hospital_Service.Doctor_Service.handlers.mqtt_handler import mqtt_client

router = APIRouter()

os.makedirs(REPORT_DIR, exist_ok=True)

@router.post("/doctor/add_report")
def add_report(report: ReportBase):
    return ReportService.add_report(report)

@router.get("/doctor/get_reports/{patient_id}")
def get_reports(patient_id: int):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
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
    return PrescriptionService.add_prescription(prescription)

@router.get("/doctor/get_patient/{patient_id}")
def get_patient(patient_id: int):
    try:
        response = requests.get(f"http://127.0.0.1:12378/patient/get_patient/{patient_id}")
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Patient not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching patient data")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Communication error with Patient Service: {str(e)}")

@router.post("/doctor/request_test/")
def request_test_api(request: TestRequest):
    return request_test(request)

@router.post("/doctor/submit_result/")
def submit_result(report_id: int, result_file: UploadFile = File(...)):
    file_path = os.path.join(REPORT_DIR, f"result_{report_id}.txt")
    with open(file_path, "wb") as f:
        f.write(result_file.file.read())

    mqtt_client.publish(MQTT_TOPIC_TEST_RESULT, json.dumps({
        "report_id": report_id,
        "file_path": file_path
    }))
    return {"message": "Test result submitted", "report_id": report_id}