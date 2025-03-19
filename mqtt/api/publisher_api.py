from fastapi import APIRouter, HTTPException
from mqtt.schemas.message_schema import Message
from mqtt.services.publisher_service import publish_message

router = APIRouter()

@router.post("/publish")
def publish_mqtt_message(message: Message):
    try:
        payload = message.model_dump()
        response = publish_message(payload)

        if response["status"] == "Failed":
            raise HTTPException(status_code=500, detail=response["error"])

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
