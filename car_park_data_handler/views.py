from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from . import mongodb_interface
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CarparkSerializer, CarparkDataSerializer
from .models import Carpark, CarparkData

import logging

import requests
import time
import datetime

# environment variables and constants
import os
import dotenv

# set up logger
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"


def carpark_id(cp):
    """input = dict of carpark, in the API format. output = string to be used in DB as its ID"""
    return f'{cp["CarParkID"]}-{cp["LotType"]}'


def index(request):
    # members = Members.objects.all()[1:20]  # example of slicing
    # output = ', '.join([member.name for member in members])
    # return HttpResponse(output)
    context = {"message": "Hello World! This is templating!"}
    return render(request, 'car_park_data_handler/index.html', context)

    # this should return a list of carpark ID


def detail(request, car_park_id):
    # return the time series for 1 car park
    data = mongodb_interface.get_car_park_details(car_park_id=car_park_id)
    context = {"car_park_id": car_park_id, "list_of_data": data}
    return render(request, 'car_park_data_handler/detail.html', context)
    # return HttpResponse(f'You looked for car park ID: {car_park_id}')


@csrf_exempt
def scrape(request):
    """make 1 run of the data scraper"""

    if request.method != "POST":
        return JsonResponse({'message': 'Endpoint accessed incorrectly.'})

    logger.info('Starting data scraper')

    for skip_rows in range(0, 10000, 500):
        # used a for loop to prevent infinite loops, and also elegantly iterate the skip_rows variable

        # call API
        request_time = int(time.time())
        logger.info(f'Calling {API_URL}?$skip={skip_rows}')
        response = requests.get(f'{API_URL}?$skip={skip_rows}', headers={"AccountKey": LTA_ACCOUNT_KEY})

        # only proceed if response is successful
        if response.status_code == 200:
            api_data = response.json()["value"]

            # if we got data, then save it. Otherwise, stop the loop
            logger.debug(f"rows in response: {len(api_data)}")

            if len(api_data) == 0:
                rows_remaining_flag = False
                break

            # OK we got data. Let's transform it and put it in the DB.

            for carpark in api_data:
                # make the carpark dict
                loc_str = carpark["Location"].split()
                carpark_dict = {
                    "id": carpark_id(carpark),
                    "car_park_id": carpark["CarParkID"],
                    "area": carpark["Area"],
                    "development": carpark["Development"],
                    "location_lat": float(loc_str[0]),
                    "location_lon": float(loc_str[1]),
                    "lot_type": carpark["LotType"],
                    "agency": carpark["Agency"]
                }

                # add the carpark to the db if it is new
                try:
                    # get the matching one from DB, if it exists.
                    carpark_db = Carpark.objects.get(id=carpark_id(carpark)).__dict__
                    carpark_db.pop('_state')  # remove extra things that the Model has
                    # Compare differences
                    if carpark_dict != carpark_db:
                        logger.error(
                            "New carpark data from API is different from database! Please take action to resolve.")
                        logger.debug("Database version:")
                        logger.debug(carpark_db)
                        logger.debug("API version:")
                        logger.debug(carpark_dict)
                except Carpark.DoesNotExist:
                    logger.warning(f"Carpark ID {carpark_id(carpark)} not found, adding it to DB.")

                    # try to save the Carpark object
                    serializer = CarparkSerializer(data=carpark_dict)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.error(f"Error with saving Carpark to database. Serializer error: {serializer.errors}")
                        logger.debug(carpark)
                        logger.debug(carpark_dict)

                # make the carparkData dict
                carpark_data_dict = {
                    "carpark_id": carpark_id(carpark),
                    "available_lots": carpark["AvailableLots"],
                    "timestamp": datetime.datetime.utcfromtimestamp(request_time)
                }

                serializer = CarparkDataSerializer(data=carpark_data_dict)
                if serializer.is_valid():
                    serializer.save()
                else:
                    logger.error(f"Error with saving CarparkData to database. Serializer error: {serializer.errors}")
                    logger.debug(carpark)
                    logger.debug(carpark_dict)
        else:
            logger.error(f"API was not reached. Status code: {response.status_code}")

    logger.info("Data scraping complete")

    return JsonResponse({'message': 'You have reached the data scraper endpoint.'})
