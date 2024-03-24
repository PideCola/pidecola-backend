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
                ride_requests = RideRequest.objects.filter(~Q(status="cancelado") & ~Q(status="finalizado") & Q(origin=origin) & Q(destination=destination))
            else:
                ride_requests = RideRequest.objects.filter(~Q(status="cancelado") & ~Q(status="finalizado") )

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
    def active(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            ride_requests = RideRequest.objects.filter(Q(user=user) & ~Q(status="cancelado") & Q(is_reviewed=False))

            # Serialize the first active request (if available)
            if len(ride_requests) > 0:
                first_ride_request = ride_requests[0]
                serialized_request = RideRequestSerializer(first_ride_request).data
                serialized_request['origin'] = first_ride_request.origin.name
                serialized_request['destination'] = first_ride_request.destination.name
                if first_ride_request.ride is not None:
                    user_info = {
                        'id': first_ride_request.ride.driver.id,
                        'first_name': first_ride_request.ride.driver.first_name,
                        'last_name': first_ride_request.ride.driver.last_name,
                        'phone_number': first_ride_request.ride.driver.phone_number
                    }
                    serialized_request['driver'] = user_info
                return Response(serialized_request, status=status.HTTP_200_OK)
            else:
                return Response({}, status=status.HTTP_200_OK)
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

    @action(methods=['PATCH'], detail=True)
    def review(self, request, pk=None):
        valoration = request.data.get("review")
        try:
            ride_request = RideRequest.objects.get(pk=pk)
            driver = ride_request.ride.driver
            if (valoration == "like"):
                driver.likes += 1
            elif (valoration == "dislike"):
                driver.dislikes += 1
            driver.save()
            ride_request.is_reviewed = True
            ride_request.save()
            return Response({"message": "Valoración realizada"}, status=status.HTTP_200_OK)
        except RideRequest.DoesNotExist:
            return Response({"message": "La solicitud no existe"}, status=status.HTTP_404_NOT_FOUND)

class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_id = request.data.get("user")
        origin_name = request.data.get("origin")
        destination_name = request.data.get("destination")
        requests = request.data.get("requests")

        try:
            driver = User.objects.get(pk=user_id)
            origin_route = Route.objects.get(name=origin_name)
            destination_route = Route.objects.get(name=destination_name)

        except Route.DoesNotExist:
            return Response({"message": "La ruta de origen o destino no existe"}, status=status.HTTP_400_BAD_REQUEST)

        ride = Ride.objects.create(
            driver=driver,
            origin=origin_route,
            destination=destination_route
        )
        ride.save()

        try:
            # For each ride_request id, change status to "aceptado" and add ride to it
            for request_id in requests:
                ride_request = RideRequest.objects.get(pk=request_id)
                ride_request.status = RideRequest.ACCEPTED
                ride_request.ride = ride
                ride_request.save()
        except Ride.DoesNotExist:
            return Response({"message": "La solicitud de cola no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def get_by_user_id(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            rides = Ride.objects.filter(Q(driver=user) & ~Q(status="finalizado"))

            serialized_rides = []
            for ride in rides:
                requests = RideRequest.objects.filter(Q(ride=ride))
                serialized_ride = RideSerializer(ride).data
                serialized_ride['origin'] = ride.origin.name
                serialized_ride['destination'] = ride.destination.name
                serialized_ride['passengers'] = []
                for request in requests:
                    user_info = {
                        'id': request.user.id,
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'phone_number': request.user.phone_number,
                    }
                    serialized_ride['passengers'].append(user_info)

                serialized_rides.append(serialized_ride)

            return Response(serialized_rides, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PATCH'], detail=True)
    def initiate(self, request, pk=None):
        try:
            ride = Ride.objects.get(pk=pk)
            ride.status = Ride.STARTED
            ride.save()
            requests = RideRequest.objects.filter(ride=ride)
            for request in requests:
                request.status = RideRequest.STARTED
                request.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
        except RideRequest.DoesNotExist:
            return Response({"message": "La cola no existe"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PATCH'], detail=True)
    def finish(self, request, pk=None):
        try:
            ride = Ride.objects.get(pk=pk)
            ride.status = Ride.FINISHED
            ride.save()
            requests = RideRequest.objects.filter(ride=ride)
            for request in requests:
                request.status = RideRequest.FINISHED
                request.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
        except RideRequest.DoesNotExist:
            return Response({"message": "La solicitud no existe"}, status=status.HTTP_404_NOT_FOUND)
