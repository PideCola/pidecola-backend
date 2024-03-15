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

    @action(detail=True, methods=['GET'])
    def vehicles(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            vehicles_data = VehicleSerializer(user.vehicles.all(), many=True).data
            return Response(vehicles_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

