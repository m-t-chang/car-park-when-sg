import django.db.utils
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
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    def delete(self, request):
        if request.user.is_superuser:
            return Response(
                {"status": "failure", "message": "Cannot delete superuser this way.", "email": request.user.email})
        
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)


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
