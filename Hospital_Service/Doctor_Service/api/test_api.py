import json
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from Hospital_Service.Doctor_Service.config.constants import REPORT_DIR, MQTT_TOPIC_TEST_RESULT
from Hospital_Service.Doctor_Service.handlers.mqtt_handler import mqtt_client

router = APIRouter()

os.makedirs(REPORT_DIR, exist_ok=True)

@router.get("/download_report/{file_name}")
def download_report(file_name: str):
    file_path = os.path.join(REPORT_DIR, file_name)

    if os.path.exists(file_path):
        try:
            report_id = int(file_name.split("_")[-1].split(".")[0])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid file name format")

        payload = json.dumps({"report_id": report_id, "result": file_path})
        mqtt_client.publish(MQTT_TOPIC_TEST_RESULT, payload)

        return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="File not found")