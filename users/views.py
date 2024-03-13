from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User, Vehicle
from users.serializers import UserSerializer, VehicleSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['get'])
    def vehicles(self, request, pk):
        user = User.objects.get(pk=pk)
        vehicles = VehicleSerializer(user.vehicles.all(), many=True).data
        return Response(vehicles, status=status.HTTP_200_OK)


class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
