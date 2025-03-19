import json
import sqlite3

from Doctor_Patient_System.handlers.handler import mqtt_client
from Doctor_Patient_System.config.constants import MQTT_TOPIC_TEST_REQUEST, DATABASE_FILE1
from Doctor_Patient_System.scripts.init_db import initialize_db_1


def request_test(request):
    db = sqlite3.connect(DATABASE_FILE1)
    cursor = db.cursor()
    cursor.execute("INSERT INTO reports (patient_id, doctor_id, test_type, test_details, date) VALUES (?, ?, ?, ?, ?)",
                   (request.patient_id, request.doctor_id, request.test_type, request.test_details, request.date))
    db.commit()
    report_id = cursor.lastrowid
    db.close()

    mqtt_client.publish(MQTT_TOPIC_TEST_REQUEST, json.dumps({
        "report_id": report_id,
        "patient_id": request.patient_id,
        "doctor_id": request.doctor_id,
        "test_type": request.test_type
    }))
    return {"message": "Test requested", "report_id": report_id}


def get_report(report_id):
    db = initialize_db_1()
    conn = sqlite3.connect(DATABASE_FILE1)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
    report = cursor.fetchone()
    conn.close()
    print(type(report), report)

    if report:
        return {
            "report_id": report["id"],
            "patient_id": report["patient_id"],
            "doctor_id": report["doctor_id"],
            "test_type": report["test_type"],
            "test_details": report["test_details"],
            "result": report["result"]
        }
    return None