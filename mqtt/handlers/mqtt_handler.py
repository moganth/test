from pymongo import MongoClient
import json
# from mqtt.config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME
from mqtt.config.settings import MqttConstants, MongoConstants
from mqtt.utils.logger import logger

mq = MqttConstants()
mo = MongoConstants()

mongo_client = MongoClient(mo.MONGO_URI)
db = mongo_client[mo.DB_NAME]
collection = db[mo.COLLECTION_NAME]


def process_message(payload: str):
    try:
        data = json.loads(payload)

        if "data" not in data or "student_id" not in data["data"]:
            logger.error("Invalid data format, missing 'data' or 'student_id'")
            return

        student_id = data["data"]["student_id"]

        collection.update_one(
            {"data.student_id": student_id},
            {"$set": data},
            upsert=True
        )

        logger.info(f"Message processed and stored: {data}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
