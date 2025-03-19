from pymongo import MongoClient
from mqtt.config.settings import MqttConstants, MongoConstants
# from mqtt.config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME

mq = MqttConstants()
mo = MongoConstants()

mongo_client = MongoClient(mo.MONGO_URI)
db = mongo_client[mo.DB_NAME]
collection = db[mo.COLLECTION_NAME]
