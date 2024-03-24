from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rides.models import Ride, RideRequest
from users.models import User, Vehicle
from users.serializers import UserSerializer, VehicleSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['get', 'post'])
    def vehicles(self, request, pk):
        if request.method == 'GET':
            user = User.objects.get(pk=pk)
        vehicles = VehicleSerializer(user.vehicles.all(), many=True).data
        return Response(vehicles, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def has_ride_or_request(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            has_ride = Ride.objects.filter(Q(driver=user) & (Q(status="pendiente") | Q(status="iniciado"))).exists()
            has_request = RideRequest.objects.filter(Q(user=user) & (Q(status="pendiente") | Q(status="aceptado") | Q(status="iniciado"))).exists()
            return Response({"ride": has_ride, "request": has_request}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

