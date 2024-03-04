from django.shortcuts import render
from rest_framework import viewsets

from rides.models import Route, RideRequest, Ride
from rides.serializers import RouteSerializer, RideRequestSerializer, RideSerializer
from custom import CustomPermission

# Create your views here.
class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = [CustomPermission]

class RideRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RideRequestSerializer
    queryset = RideRequest.objects.all()
    permission_classes = [CustomPermission]

class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = [CustomPermission]
