from pymongo import MongoClient
from pprint import pprint
import requests
import time
import os
import dotenv

# environment variables and constants
dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"

if __name__ == '__main__':
    # connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client.car_park_when_sg

    # call the api
    print("Calling API...")
    request_time = int(time.time())
    response = requests.get(API_URL, headers={"AccountKey": LTA_ACCOUNT_KEY})
    print("API response status code: ", response.status_code)

    # only proceed if response is successful
    if response.status_code == 200:
        api_data = response.json()["value"]
        # pprint(api_data[1])  # view one object in the response

        print(request_time)
        # wrap the result
        doc_to_insert = {"timestamp": request_time, "data": api_data}

        # save to db and check result
        result = db.api_responses.insert_one(doc_to_insert)
        pprint(result)
