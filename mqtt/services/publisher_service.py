import paho.mqtt.client as mqtt
import json
from mqtt.config.settings import MqttConstants
from mqtt.utils.logger import logger

mq = MqttConstants()

def publish_message(payload: dict):
    try:
        client = mqtt.Client()
        client.connect(mq.MQTT_BROKER, mq.MQTT_PORT, 60)

        payload_json = json.dumps(payload)
        client.publish(mq.MQTT_TOPIC, payload_json)
        logger.info(f"Published Message: {payload_json}")

        return {"status": "Message published", "data": payload}
    except Exception as e:
        logger.error(f"Error publishing message: {e}")
        return {"status": "Failed", "error": str(e)}
