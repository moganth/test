import paho.mqtt.client as mqtt

from mqtt.config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from mqtt.handlers.mqtt_handler import on_message
from mqtt.utils.logger import logger

def start_consumer():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)

    logger.info("MQTT Consumer Started...")
    client.loop_start()
