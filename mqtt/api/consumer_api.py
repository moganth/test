from fastapi import APIRouter, HTTPException
import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
# from mqtt.config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from mqtt.utils.logger import logger
from mqtt.config.settings import MqttConstants, MongoConstants

mq = MqttConstants()
mo = MongoConstants()

router = APIRouter()

mongo_client = MongoClient(mo.MONGO_URI)
db = mongo_client[mo.DB_NAME]
collection = db[mo.COLLECTION_NAME]

mqtt_client = mqtt.Client()


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))

        if "data" not in payload or "student_id" not in payload["data"]:
            logger.error("Invalid message format: missing 'data' or 'student_id'")
            return

        student_id = payload["data"]["student_id"]

        collection.update_one(
            {"data.student_id": student_id},
            {"$set": payload},
            upsert=True
        )

        logger.info(f"Message received and stored: {payload}")
    except Exception as e:
        logger.error(f"Error processing received MQTT message: {e}")

def start_mqtt_consumer():
    mqtt_client.on_message = on_message
    mqtt_client.connect(mq.MQTT_BROKER, mq.MQTT_PORT, 60)
    mqtt_client.subscribe(mq.MQTT_TOPIC)
    mqtt_client.loop_start()
    logger.info("MQTT Consumer Started...")

start_mqtt_consumer()


@router.get("/messages")
def get_messages():
    try:
        messages = list(collection.find({}, {"_id": 0}))
        if not messages:
            return {"message": "No records found"}
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")
