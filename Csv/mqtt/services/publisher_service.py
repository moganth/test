import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

from mqtt.config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from mqtt.constants import ATTENDANCE_STATUSES
from mqtt.utils.logger import logger

def generate_student_id():
    return random.randint(100, 500)

def generate_dob():
    year = random.randint(2000, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def start_publisher():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    logger.info("Student Attendance Publisher Started...")

    while True:
        message = {
            "data": {
                "student_id": generate_student_id(),
                "dob": generate_dob(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "attendance": random.choice(ATTENDANCE_STATUSES)
            },
            "condition": {
                "alert": False
            }
        }

        payload = json.dumps(message)
        client.publish(MQTT_TOPIC, payload)
        logger.info(f"Published Attendance: {payload}")
        time.sleep(5)

