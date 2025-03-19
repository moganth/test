import json
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import paho.mqtt.client as mqtt

from Doctor_Patient_System.config.constants import REPORT, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_TEST_RESULT

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

os.makedirs(REPORT, exist_ok=True)

router = APIRouter()

@router.get("/download_report/{file_name}")
def download_report(file_name: str):
    file_path = os.path.join(REPORT, file_name)

    if os.path.exists(file_path):
        try:
            report_id = int(file_name.split("_")[-1].split(".")[0])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid file name format")

        payload = json.dumps({"report_id": report_id, "result": file_path})
        mqtt_client.publish(MQTT_TOPIC_TEST_RESULT, payload)

        return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
# raise HTTPException(status_code=404, detail="File not found")