from rest_framework.routers import DefaultRouter
from rides.views import RouteViewSet, RideRequestViewSet, RideViewSet

router = DefaultRouter()
router.register('routes', RouteViewSet)
router.register('ride_requests', RideRequestViewSet)
router.register('rides', RideViewSet)