import json

from mqtt.models.database import collection
from mqtt.utils.logger import logger

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)

        collection.insert_one(data)

        logger.info(f"New data saved to MongoDB: {data}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
