from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User, Vehicle
from users.serializers import UserSerializer, VehicleSerializer
from custom import CustomPermission

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [CustomPermission]


class VehicleViewSet(viewsets.ModelViewSet):

    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [CustomPermission]
