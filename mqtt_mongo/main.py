import paho.mqtt.client as mqtt
import json
import time
from pymongo import MongoClient

# MQTT Configuration
MQTT_BROKER = "135.235.145.253"
MQTT_PORT = 1883
MQTT_TOPIC = "test/data"

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "mqtt_data"
COLLECTION_NAME = "messages"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


# MQTT Consumer Callback (Receives Messages)
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)

        # Insert a new record instead of updating an existing one
        collection.insert_one(data)

        print(f"New data saved to MongoDB: {data}")

    except Exception as e:
        print(f"Error processing message: {e}")



# Function to Start MQTT Consumer
def start_consumer():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)

    print("MQTT Consumer Started...")
    client.loop_start()  # Start MQTT loop in background


# Function to Start MQTT Publisher
def start_publisher():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("MQTT Publisher Started...")

    while True:
        # Generate sensor data
        message = {
            "data": {
                "sensor_id": 1001,
                "temperature": round(20 + 5 * time.time() % 10, 2),
                "humidity": round(50 + 10 * time.time() % 10, 2)
            },
            "condition": {
                "alert": False
            }
        }

        # Publish message
        payload = json.dumps(message)
        client.publish(MQTT_TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(5)  # Publish every 5 seconds


# Run Both Publisher & Consumer in the Same Script
if __name__ == "__main__":
    start_consumer()  # Start MQTT consumer (listens for messages)
    start_publisher()  # Start MQTT publisher (publishes messages)
