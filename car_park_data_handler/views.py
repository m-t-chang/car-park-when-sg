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

from pymongo import MongoClient
from django.db import connection
from django.db import transaction

# environment variables and constants
import os
import dotenv

# set up logger
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
LTA_ACCOUNT_KEY = os.environ.get("LTA_ACCOUNT_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")
API_URL = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"


def make_carpark_id(cp):
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
