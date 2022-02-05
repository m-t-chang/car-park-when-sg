from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from . import mongodb_interface

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CarparkSerializer, CarparkDataSerializer
from .models import Carpark, CarparkData

from pprint import pprint
import requests
import time
import datetime

# environment variables and constants
import os
import dotenv

dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"


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


def scrape(request):
    """make 1 run of the data scraper"""

    rows_remaining_flag = True
    skip_rows = 0
    while rows_remaining_flag:
        # DEBUG
        print(f'skip rows = {skip_rows}')

        # call API
        request_time = int(time.time())
        print(f'Calling API at {API_URL}?$skip={skip_rows}')
        response = requests.get(f'{API_URL}?$skip={skip_rows}', headers={"AccountKey": LTA_ACCOUNT_KEY})
        print("API response status code: ", response.status_code)

        # only proceed if response is successful
        if response.status_code == 200:
            api_data = response.json()["value"]

            # if we got data, then save it. Otherwise, stop the loop
            print(f"rows in response: {len(api_data)}")

            if len(api_data) == 0:
                rows_remaining_flag = False
            else:
                # OK we got data. Let's transform it and put it in the DB.
                # LEFT OFF HERE

                for carpark in api_data:

                    # make the carpark dict
                    loc_str = carpark["Location"].split()
                    carpark_dict = {
                        "id": f'{carpark["CarParkID"]}-{carpark["LotType"]}',
                        "car_park_id": carpark["CarParkID"],
                        "area": carpark["Area"],
                        "development": carpark["Development"],
                        "location_lat": loc_str[0],
                        "location_lon": loc_str[1],
                        "lot_type": carpark["LotType"],
                        "agency": carpark["Agency"]
                    }

                    # try to save the Carpark object
                    serializer = CarparkSerializer(data=carpark_dict)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        pprint(carpark)
                        pprint(carpark_dict)
                        pprint("Error with creating")

                        pprint(serializer.errors)
                        # return JsonResponse({'message': 'Some Error'})

                    # make the carparkData dict
                    carpark_data_dict = {
                        "carpark_id": f'{carpark["CarParkID"]}-{carpark["LotType"]}',
                        "available_lots": carpark["AvailableLots"],
                        "timestamp": datetime.datetime.utcfromtimestamp(request_time)
                    }

                    serializer = CarparkDataSerializer(data=carpark_data_dict)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        pprint(carpark)
                        pprint(carpark_data_dict)
                        pprint("Error with creating")
                        pprint(serializer.errors)
                        # return JsonResponse({'message': 'Some Error'})

            # #### CODE FROM CLASS
            # serializer = CarparkSerializer(data=api_data[0])
            #
            # # without the .is_valid, then django will throw an error of "you did not check if serializer is valid before saving"
            # if serializer.is_valid():
            #     serializer.save()
            #
            #     return Response(serializer.data)
            #
            # else:
            #     return Response('Error with creating')

            ## END CODE FROM CLASS

            # wrap the result
            doc_to_insert = {"timestamp": request_time, "data": api_data}

            # save to db and check result
            ## DONT INSERT FOR NOW
            # result = db.api_responses.insert_one(doc_to_insert)
            # pprint(result)

            # set the skip parameter to get the next 500 rows
            skip_rows += 500

    return JsonResponse({'message': 'You''ve reached the placeholder for the data scraping endpoint.'})
