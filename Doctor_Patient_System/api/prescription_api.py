import sqlite3
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import pandas as pd

from Doctor_Patient_System.config.constants import DATABASE_FILE
from Doctor_Patient_System.services.prescription_service import PrescriptionService
from Doctor_Patient_System.utils.logger import logger

router = APIRouter()

@router.get("/patient/get_prescriptions/{patient_id}")
def get_prescriptions(patient_id: int):
    prescriptions = PrescriptionService.get_prescriptions_by_patient(patient_id)
    if not prescriptions:
        raise HTTPException(status_code=404, detail="No prescriptions found for this patient")
    return prescriptions


@router.get("/patient/download_prescriptions/{patient_id}")
def download_prescriptions(patient_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescriptions WHERE patient_id = ?", (patient_id,))
    prescriptions = cursor.fetchall()
    conn.close()
    logger.info("Fetched Prescriptions:", prescriptions)

    if not prescriptions:
        logger.error("No prescriptions found for this patient!")
        return {"message": f"No prescriptions found for patient ID {patient_id}"}

    columns = ["id", "patient_id", "doctor_id", "prescription_details", "created_at"]
    df = pd.DataFrame(prescriptions, columns=columns)
    logger.error(df)
    excel_path = f"prescriptions_patient_{patient_id}.xlsx"
    df.to_excel(excel_path, index=False)
    logger.info(f"Excel saved at: {excel_path}")
    return FileResponse(excel_path, filename=f"prescriptions_{patient_id}.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
