from pymongo import MongoClient

# pprint library is used to make the output look more pretty
from pprint import pprint

# for the sample code
from random import randint

import requests
import os
import dotenv

dotenv.load_dotenv()

os.environ.get("api-token")

# constnats
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"


def generate_sample_code():
    # LEFT OFF CODE
    # Step 1: Connect to MongoDB - Note: Change connection string as needed
    client = MongoClient(port=27017)
    db = client.business
    # Step 2: Create sample data
    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City', 'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich',
             'Lazy', 'Fun']
    company_type = ['LLC', 'Inc', 'Company', 'Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    for x in range(1, 501):
        business = {
            'name': names[randint(0, (len(names) - 1))] + ' ' + names[randint(0, (len(names) - 1))] + ' ' +
                    company_type[randint(0, (len(company_type) - 1))],
            'rating': randint(1, 5),
            'cuisine': company_cuisine[randint(0, (len(company_cuisine) - 1))]
        }
        # Step 3: Insert business object directly into MongoDB via insert_one
        result = db.reviews.insert_one(business)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created {0} of 500 as {1}'.format(x, result.inserted_id))
    # Step 5: Tell us that you are done
    print('finished creating 500 business reviews')


def scrape(api_url):
    # PSEUDOCODE FOR SCRAPING SCRIPT
    # Use MongoDB for rapid spin-up. I will try using multiple DB
    #
    #   I want to save the API output. And timestamp it.
    #   Then have it run regularly on Heroku.
    #

    # I got MongoDB working!

    # call the api
    print("calling api")
    response = requests.get(api_url)

    print(response)

    # error handling, like if the response status is not 200
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
    else:
        data_to_be_used = response.json()
        pprint(data_to_be_used)
        # save it into DB

        # do some logging

        # let's get the data out
        for item in data_to_be_used:
            print(item)

        for item in data_to_be_used["people"]:
            print(item["name"])


if __name__ == '__main__':
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    MONGODB_URI = "mongodb://localhost:27017"
client = MongoClient(MONGODB_URI)
db = client.admin
# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

# generate_sample_code()

scrape(API_URL)
