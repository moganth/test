import os
import sqlite3
import paho.mqtt.client as mqtt
import json

from Doctor_Patient_System.config.constants import MQTT_BROKER, MQTT_PORT, DATABASE_FILE1, TEST
from Doctor_Patient_System.config.constants import MQTT_TOPIC_TEST_SUBMISSION, MQTT_TOPIC_TEST_RESULT


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC_TEST_SUBMISSION)
    client.subscribe(MQTT_TOPIC_TEST_RESULT)


def on_message(client, userdata, msg):
    db = sqlite3.connect(DATABASE_FILE1)
    cursor = db.cursor()
    payload = json.loads(msg.payload.decode())

    report_id = payload["report_id"]

    if msg.topic == MQTT_TOPIC_TEST_SUBMISSION:
        file_path = os.path.join(TEST, f"test_details_{report_id}.txt")
        cursor.execute("UPDATE reports SET test_details=? WHERE id=?", (file_path, report_id))

    elif msg.topic == MQTT_TOPIC_TEST_RESULT:
        result_file_path = os.path.join(TEST, f"test_result_{report_id}.txt")
        cursor.execute("UPDATE reports SET result=? WHERE id=?", (result_file_path, report_id))

    db.commit()
    db.close()


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()
