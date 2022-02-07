from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from car_park_data_handler.serializers import CarparkSerializer
from car_park_data_handler.models import Carpark


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


# APIs for frontend
class CarparkList(APIView):
    # this 1 line is all you need to protect API endpoint
    # also, note that this authentication will apply to all methods in this class
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        carparks = Carpark.objects.all()
        serializer = CarparkSerializer(carparks, many=True)

        return Response(serializer.data)
