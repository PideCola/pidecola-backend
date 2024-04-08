from .routes_settings import default_routes
from rides.models import Route

def routes_setup():
    routes = [Route(name=name) for name in default_routes]
    Route.objects.bulk_create(routes)