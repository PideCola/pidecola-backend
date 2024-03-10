from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import Response
from rest_framework.permissions import IsAuthenticated
from rides.models import Route, RideRequest, Ride
from rides.serializers import RouteSerializer, RideRequestSerializer, RideSerializer
from custom import CustomPermission
from users.models import User

# Create your views here.
class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = [IsAuthenticated]

class RideRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RideRequestSerializer
    queryset = RideRequest.objects.all()

    def create(self, request):
        user_id = request.data.get("user")
        origin_name = request.data.get("origin")
        destination_name = request.data.get("destination")

        try:
            user = User.objects.get(pk=user_id)
            origin_route = Route.objects.get(name=origin_name)
            destination_route = Route.objects.get(name=destination_name)
        except Route.DoesNotExist:
            return Response({"message": "La ruta de origen o destino no existe"}, status=status.HTTP_400_BAD_REQUEST)

        ride_request = RideRequest.objects.create(
            user=user,
            origin=origin_route,
            destination=destination_route
        )
        ride_request.save()
        
        return Response(RideRequestSerializer(ride_request).data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def get_by_user_id(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            ride_requests = RideRequest.objects.filter(user=user)

            # Serialize ride requests with additional route names
            serialized_requests = []
            for ride_request in ride_requests:
                serialized_request = RideRequestSerializer(ride_request).data
                serialized_request['origin'] = ride_request.origin.name
                serialized_request['destination'] = ride_request.destination.name
                serialized_requests.append(serialized_request)

            return Response(serialized_requests, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = [IsAuthenticated]

