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

    # scrape the API once
    # PSEUDOCODE FOR SCRAPING
    # Use MongoDB for rapid spin-up. I will try using multiple DB
    #
    #   I want to save the API output. And timestamp it.
    #   Then have it run regularly on Heroku.
    #
    # I got MongoDB working!

    ######### NEW

    rowsRemainingFlag = True
    skipRows = 0
    while rowsRemainingFlag:
        # DEBUG
        print(f'skip rows = {skipRows}')

        # call API
        request_time = int(time.time())
        print(f'Calling API at {API_URL}?$skip={skipRows}')
        response = requests.get(f'{API_URL}?$skip={skipRows}', headers={"AccountKey": LTA_ACCOUNT_KEY})
        print("API response status code: ", response.status_code)

        # only proceed if response is successful
        if response.status_code == 200:
            api_data = response.json()["value"]

            # if we got data, then save it. Otherwise, stop the loop
            print(f"rows in response: {len(api_data)}")

            if len(api_data) == 0:
                rowsRemainingFlag = False
            else:
                # OK we got data. Let's transform it and put it in the DB.
                # LEFT OFF HERE

                # wrap the result
                doc_to_insert = {"timestamp": request_time, "data": api_data}

                # save to db and check result
                ## DONT INSERT FOR NOW
                # result = db.api_responses.insert_one(doc_to_insert)
                # pprint(result)

                # set the skip parameter to get the next 500 rows
                skipRows += 500

        # ######### END NEW
        #
        # # call the api
        # print("Calling API...")
        # request_time = int(time.time())
        # response = requests.get(API_URL, headers={"AccountKey": LTA_ACCOUNT_KEY})
        # print("API response status code: ", response.status_code)
        #
        # # only proceed if response is successful
        # if response.status_code == 200:
        #     api_data = response.json()["value"]
        # # pprint(api_data[1])  # view one object in the response
        #
        # print(request_time)
        # # wrap the result
        # doc_to_insert = {"timestamp": request_time, "data": api_data}
        #
        # # save to db and check result
        # result = db.api_responses.insert_one(doc_to_insert)
        # pprint(result)
