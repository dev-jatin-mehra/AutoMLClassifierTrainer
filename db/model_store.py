from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DBNAME")]
models_collection = db["MONGO_COLLECTION"]

def save_model_metadata(**kwargs):
    if models_collection.find_one({"filename": kwargs["filename"], "target": kwargs["target"]}):
        return False
    models_collection.insert_one({
        **kwargs,
        "uploaded_at": datetime.now()
    })
    return True

def get_all_models():
    return list(models_collection.find({}, {"_id": 0}).sort("uploaded_at", -1))
