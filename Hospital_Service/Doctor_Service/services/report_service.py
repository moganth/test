import json
import sqlite3
from Hospital_Service.Doctor_Service.config.constants import DATABASE_FILE, MQTT_TOPIC_TEST_REQUEST
from Hospital_Service.Doctor_Service.handlers.mqtt_handler import mqtt_client

class ReportService:
    @staticmethod
    def add_report(report_data):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reports (patient_id, test_name, disease, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                report_data.patient_id, report_data.test_name, report_data.disease,
                report_data.created_at
            ))
            conn.commit()
            return {"message": "Report added successfully"}
        except sqlite3.IntegrityError:
            return {"error": "Integrity constraint violated (e.g., invalid patient ID)"}
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}
        finally:
            conn.close()

    @staticmethod
    def get_reports_by_patient(patient_id):
        try:
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE patient_id=?", (patient_id,))
            reports = cursor.fetchall()
            if not reports:
                return {"message": "No reports found for the given patient ID"}

            column_names = [column[0] for column in cursor.description]
            return [dict(zip(column_names, report)) for report in reports]
        except sqlite3.Error as e:
            return {"error": f"Database error: {str(e)}"}
        finally:
            conn.close()

def request_test(request):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_requests (patient_id, doctor_id, test_type, test_details, date) VALUES (?, ?, ?, ?, ?)",
                   (request.patient_id, request.doctor_id, request.test_type, request.test_details, request.date))
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()

    mqtt_client.publish(MQTT_TOPIC_TEST_REQUEST, json.dumps({
        "report_id": report_id,
        "patient_id": request.patient_id,
        "doctor_id": request.doctor_id,
        "test_type": request.test_type
    }))
    return {"message": "Test requested", "report_id": report_id}