from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet)
router.register(r'vehicles', VehicleViewSet)