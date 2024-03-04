from rest_framework import serializers
from rides.models import Route, RideRequest, Ride

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
