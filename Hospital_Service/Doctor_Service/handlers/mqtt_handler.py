import os
import sqlite3
import paho.mqtt.client as mqtt
import json

from Hospital_Service.Doctor_Service.config.constants import MQTT_BROKER, MQTT_PORT, DATABASE_FILE, MQTT_TOPIC_TEST_RESULT
from Hospital_Service.Doctor_Service.utils.logger import logger


def on_connect(client, userdata, flags, rc):
    logger.info("Doctor Service connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC_TEST_RESULT)


def on_message(client, userdata, msg):
    logger.info(f"Message received on topic: {msg.topic}")

    try:
        payload = json.loads(msg.payload.decode())
        report_id = payload.get("report_id")

        if msg.topic == MQTT_TOPIC_TEST_RESULT:
            result_file_path = payload.get("file_path")

            if report_id and result_file_path:
                conn = sqlite3.connect(DATABASE_FILE)
                cursor = conn.cursor()
                cursor.execute("UPDATE test_requests SET result=? WHERE id=?", (result_file_path, report_id))
                conn.commit()
                conn.close()
                logger.info(f"Updated test result for report ID: {report_id}")
    except Exception as e:
        logger.error(f"Error processing MQTT message: {str(e)}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def start_mqtt_client():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        logger.info("MQTT client started")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {str(e)}")