import paho.mqtt.client as mqtt
import json
from mqtt.models.database import collection
from mqtt.utils.logger import logger
# from mqtt.config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from mqtt.config.settings import MqttConstants, MongoConstants

mq = MqttConstants()
mo = MongoConstants()

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        collection.update_one({"data.student_id": data["data"]["student_id"]}, {"$set": data}, upsert=True)
        logger.info(f"Message received and saved: {data}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


def start_consumer():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(mq.MQTT_BROKER, mq.MQTT_PORT, 60)
    client.subscribe(mq.MQTT_TOPIC)

    logger.info("MQTT Consumer Started...")
    client.loop_start()
