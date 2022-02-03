from django.http import HttpResponse
from django.shortcuts import render
from . import mongodb_interface


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
