from pymongo import MongoClient
from pprint import pprint
import requests
import time
import os
import dotenv
from datetime import datetime

# environment variables and constants
dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"

if __name__ == '__main__':
    # connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client.car_park_when_sg

    ###################### EXPLORATORY ANALYSIS ####################
    # read the db - print 1 doc
    result = db.api_responses.find_one()

    # pprint(result)
    print(type(result))

    # result is dict
    pprint(result["data"][0])

    #
    set_agency = set()
    set_area = set()
    set_development = set()
    set_lot_type = set()
    set_car_park_id = set()

    # from one doc, list all the Agencies
    for lot in result["data"]:
        set_agency.add(lot["Agency"])
        set_area.add(lot["Area"])
        set_development.add(lot["Development"])
        set_lot_type.add(lot["LotType"])
        # print(f'{lot["Agency"]}: {lot["CarParkID"]}')
        set_car_park_id.add(lot["CarParkID"])
    pprint(set_agency)
    pprint(set_area)
    # pprint(set_development)
    pprint(set_lot_type)
    pprint(set_car_park_id)

    print(len(set_development))
    print(len(result["data"]))

    ###################### GET TREND ####################
    id_to_show = 'L0104'

    list_of_data = []

    for doc in db.api_responses.find():
        # pprint(doc['timestamp'])
        # dt_object = datetime.fromtimestamp(doc['timestamp'])
        # pprint(dt_object)

        available_lots = -99
        for lot in doc["data"]:
            if lot['CarParkID'] == id_to_show:
                lot_to_save = lot

        data_tuple = (doc['timestamp'], lot_to_save['AvailableLots'])
        # pprint(data_tuple)
        list_of_data.append(data_tuple)
    pprint(list_of_data)

    print("PROGRAM DONE")
