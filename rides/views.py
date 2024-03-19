from django.db.models import Q
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

    def get_queryset(self):
        return Route.objects.exclude(name="USB")

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

    def list(self, request):
        try:
            req_origin = request.query_params.get("origin")
            req_destination = request.query_params.get("destination")
            ride_requests = []
            if req_origin is not None and req_destination is not None:
                origin = Route.objects.get(name=req_origin)
                destination = Route.objects.get(name=req_destination)
                ride_requests = RideRequest.objects.filter(~Q(status="cancelado") & Q(origin=origin) & Q(destination=destination))
            else:
                ride_requests = RideRequest.objects.filter(~Q(status="cancelado"))

            serialized_requests = []
            for ride_request in ride_requests:
                serialized_request = RideRequestSerializer(ride_request).data
                # Return routes names
                serialized_request['origin'] = ride_request.origin.name
                serialized_request['destination'] = ride_request.destination.name
                serialized_requests.append(serialized_request)
                # Include user info
                user_info = {
                    'id': ride_request.user.id,
                    'first_name': ride_request.user.first_name,
                    'last_name': ride_request.user.last_name
                }
                serialized_request['user'] = user_info

            return Response(serialized_requests, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=True)
    def get_by_user_id(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            ride_requests = RideRequest.objects.filter(Q(user=user) & ~Q(status="cancelado"))

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

    @action(methods=['PATCH'], detail=True)
    def cancel(self, request, pk=None):
        try:
            ride_request = RideRequest.objects.get(pk=pk)
            ride_request.status = RideRequest.CANCELLED
            ride_request.save()
            return Response(RideRequestSerializer(ride_request).data, status=status.HTTP_200_OK)
        except RideRequest.DoesNotExist:
            return Response({"message": "La solicitud no existe"}, status=status.HTTP_404_NOT_FOUND)



class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = [IsAuthenticated]

