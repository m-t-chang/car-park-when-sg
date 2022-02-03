from pymongo import MongoClient
from pprint import pprint
import requests
import time
import os
import dotenv
from datetime import datetime

# environment variables and constants
dotenv.load_dotenv()
MONGODB_URI = os.environ.get("MONGODB_URI")


def get_car_park_details(car_park_id):
    # connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client.car_park_when_sg

    list_of_data = []

    for doc in db.api_responses.find():
        # pprint(doc['timestamp'])
        # dt_object = datetime.fromtimestamp(doc['timestamp'])
        # pprint(dt_object)

        for lot in doc["data"]:
            if lot['CarParkID'] == car_park_id:
                lot_to_save = lot

        data_tuple = (doc['timestamp'], lot_to_save['AvailableLots'])
        list_of_data.append(data_tuple)

    return list_of_data
