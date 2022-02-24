# Ingest data
""" This will be run as a stand-alone script.

Uses SQLAlchemy to handle database connections

"""

import requests
import time
import datetime
import MySQLdb
import dotenv
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import insert

# environment variables and constants
dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"

print('Starting data ingestion script...')

db_url = f'mysql+mysqldb://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
engine = create_engine(db_url, echo=True, future=True)
metadata_obj = MetaData()

# table reflection

carparkdata_table = Table("car_park_data_handler_carparkdata", metadata_obj, autoload_with=engine)
carpark_table = Table("car_park_data_handler_carpark", metadata_obj, autoload_with=engine)


# id is the composite one I create
# car_park_id is from LTA


def make_carpark_id(cp):
    """input = dict of carpark, in the API format. output = string to be used in DB as its ID"""
    return f'{cp["CarParkID"]}-{cp["LotType"]}'


## init data structures (lists of objects)
data_model_list = []
# carpark_id_list = list(Carpark.objects.values_list('id', flat=True))
api_data_compiled = []
carpark_data_insert_list = []
carpark_insert_list = []

# Get API Data. Combine all the pages into one list
for skip_rows in range(0, 10000, 500):
    # used a for loop to prevent infinite loops, and also elegantly iterate the skip_rows variable

    # call API
    request_time = int(time.time())
    print(f'Calling {API_URL}?$skip={skip_rows}')
    response = requests.get(f'{API_URL}?$skip={skip_rows}', headers={"AccountKey": LTA_ACCOUNT_KEY})

    # only proceed if response is successful
    if response.status_code == 200:
        api_data = response.json()["value"]

    # if we got data, then save it. Otherwise, stop the loop
    print(f"rows in response: {len(api_data)}")

    if len(api_data) == 0:
        rows_remaining_flag = False
        break

    # OK we got data. Let's transform it and put it in the DB.
    api_data_compiled.extend(api_data)

# build up a list of dicts to INSERT
for carpark in api_data_compiled:
    # make the carpark dict
    loc_str = carpark["Location"].split()
    carpark_dict = {
        "id": make_carpark_id(carpark),
        "car_park_id": carpark["CarParkID"],
        "area": carpark["Area"],
        "development": carpark["Development"],
        "location_lat": float(loc_str[0]),
        "location_lon": float(loc_str[1]),
        "lot_type": carpark["LotType"],
        "agency": carpark["Agency"]
    }

    # check if carpark is in db already. If not, add it to the list of IDs and the list to be added
    # WRITE CODE
    carpark_insert_list.append(carpark_dict)

    # make the carparkData dict, and append it to the list to be inserted
    carpark_data_insert_list.append({
        "carpark_id": make_carpark_id(carpark),
        "available_lots": carpark["AvailableLots"],
        "timestamp": datetime.datetime.utcfromtimestamp(request_time)
    })

else:
    print(f"API was not reached. Status code: {response.status_code}")

# open db connection and do inserts
with engine.begin() as conn:
    # result = conn.execute(insert_carpark_stmt)
    # result = conn.execute(insert(carpark_table), carpark_insert_list)
    result2 = conn.execute(insert(carparkdata_table), carpark_data_insert_list)

print("carpark_data len: ", len(carpark_data_insert_list))

print("Data scraping complete")

# DEBUG
import sys

sys.exit()

########## FROM TRANSFORM
## init data structures (lists of objects)
data_model_list = []
carpark_id_list = list(Carpark.objects.values_list('id', flat=True))

## get mongoDB data
client = MongoClient(MONGODB_URI)
db = client.car_park_when_sg
num_responses = db.api_responses.count_documents({})

print(f'API responses retrieved: {num_responses}')

data_insert_query = "INSERT INTO car_park_data_handler_carparkdata (carpark_id, available_lots, timestamp) VALUES "

## iterate thru each doc in the MongoDB collection, and for each one...

for index, doc in enumerate(db.api_responses.find()):

    print(f'working on {index}')

    # iterate thru each carpark in this snapshot
    for carpark in doc["data"]:
        ### (do the same as the scraper)

        # make the carpark dict
        loc_str = carpark["Location"].split()
        carpark_to_add = Carpark(
            id=make_carpark_id(carpark),
            car_park_id=carpark["CarParkID"],
            area=carpark["Area"],
            development=carpark["Development"],
            location_lat=float(loc_str[0]),
            location_lon=float(loc_str[1]),
            lot_type=carpark["LotType"],
            agency=carpark["Agency"]
        )

        # NEW VERSION (ignore potential changes, only check if ID exists)
        if make_carpark_id(carpark) not in carpark_id_list:
            logger.warning(f"Carpark ID {make_carpark_id(carpark)} not found, adding it to DB.")

            # try to save the Carpark object
            carpark_to_add.save()
            carpark_id_list.append(make_carpark_id(carpark))

        # make the carparkData dict
        data_to_add = {
            "carpark_id": make_carpark_id(carpark),
            "available_lots": carpark["AvailableLots"],
            "timestamp": datetime.datetime.utcfromtimestamp(doc['timestamp'])
        }

        data_model_list.append(data_to_add)
        data_insert_query += f"('{make_carpark_id(carpark)}', '{carpark['AvailableLots']}', '{datetime.datetime.utcfromtimestamp(doc['timestamp'])}'), "

with connection.cursor() as cursor:
    cursor.execute(data_insert_query[:-2])
