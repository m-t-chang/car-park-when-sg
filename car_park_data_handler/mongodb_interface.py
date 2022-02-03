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

        lot_to_save = {}
        for lot in doc["data"]:
            if lot['CarParkID'] == car_park_id:
                lot_to_save = lot

        data_tuple = (doc['timestamp'], lot_to_save['AvailableLots'])
        list_of_data.append(data_tuple)

    return list_of_data


def create_aggregated_data():
    """ create aggregated data, in a format for visualization"""

    # connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client.car_park_when_sg

    # init data
    # okay, the raw data is a 3D list. First index is day of week 0-6, second index is hour of day 0-23, and final index is measurement ID.
    # aggregated data is a 2D list.
    # the key is the CarParkID-LotType
    # test_data = [{   '12345-C': [[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15],[12, 14, 15]
    #                       [1, 12, 14],
    #                       [1, 12, 14],
    #                       [1, 12, 14],
    #                       [1, 12, 14],
    #                       [1, 12, 14],
    #                       [1, 12, 14]
    #                       ]},
    #             'data_aggregated':
    #             ]

    data_dict = {}
    for doc in db.api_responses.find():
        pass

# for each doc (api snapshot)
## extract the timestamp index - day of week and hour
## for each carpark
### append the availability into the right array
### move onto next


# pprint(doc['timestamp'])
# dt_object = datetime.fromtimestamp(doc['timestamp'])
# pprint(dt_object)
