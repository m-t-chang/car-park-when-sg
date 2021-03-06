import django.db.utils
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from car_park_data_handler.serializers import CarparkSerializer, CarparkDataSerializer
from car_park_data_handler.models import Carpark, CarparkData
from user_management.serializers import AccountSerializer
from user_management.models import Account
import json
from django.db.models import Avg, DateTimeField
from django.db.models.functions import ExtractHour, ExtractWeekDay


# this is overriding the default, in order to add custom claims
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add custom claims
        token['company'] = 'GA'

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserAddNew(APIView):
    def post(self, request):
        requestBody = json.loads(request.body)

        # validate the email is an email!

        try:
            user = Account.objects.create_user(requestBody["email"], requestBody["password"])
            user.save()
        except django.db.utils.IntegrityError as err:
            return Response(
                {"status": "fail", "message": "User already exists with that email! Please log in",
                 "email": requestBody["email"]})

        return Response(
            {"status": "success", "message": "New user successfully created.", "email": requestBody["email"]})


class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        print(request.data)

        request.user.email = request.data["email"]
        request.user.name = request.data["name"]
        request.user.surname = request.data["surname"]
        request.user.save()

        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    def delete(self, request):
        if request.user.is_superuser:
            return Response(
                {"status": "failure", "message": "Cannot delete superuser this way.", "email": request.user.email})

        request.user.delete()

        # logout

        return Response({"status": "success", "message": "User deleted.", "email": request.user.email})


# APIs for frontend
class CarparkList(APIView):
    # this 1 line is all you need to protect API endpoint
    # also, note that this authentication will apply to all methods in this class
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        carparks = Carpark.objects.all()
        serializer = CarparkSerializer(carparks, many=True)

        return Response(serializer.data)


class CarparkDetail(APIView):
    """returns JSON with two keys, timestamp and available_lots, with value being an array for each"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, carpark_id):
        data = CarparkData.objects.filter(carpark_id=carpark_id)
        aggregated = {"timestamp": list(data.values_list('timestamp', flat=True)),
                      "available_lots": list(data.values_list('available_lots', flat=True))}

        return Response(aggregated)


class CarparkHourlyAverage(APIView):
    """returns JSON with 7 keys, timestamp and available_lots, with value being an array for each"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, carpark_id):
        data = CarparkData.objects.filter(carpark_id=carpark_id)

        result = list(
            data.annotate(weekday=ExtractWeekDay('timestamp')).annotate(hour=ExtractHour('timestamp')).values(
                'weekday', 'hour').annotate(
                Avg('available_lots')).order_by('weekday', 'hour'))

        return JsonResponse({"data": result})
