from pymongo import MongoClient
from mqtt.config.settings import MONGO_URI, DB_NAME, COLLECTION_NAME

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]
