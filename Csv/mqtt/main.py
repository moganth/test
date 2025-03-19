from mqtt.services.consumer_service import start_consumer
from mqtt.services.publisher_service import start_publisher

if __name__ == "__main__":
    start_consumer()
    start_publisher()
