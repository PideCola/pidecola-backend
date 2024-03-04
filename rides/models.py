from django.db import models
from users.models import User

# Create your models here.
class Route(models.Model):
    name = models.CharField(max_length=32)

class RideRequest(models.Model):
    user = models.ForeignKey(User, related_name='ride_requests', on_delete=models.DO_NOTHING)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

class Ride(models.Model):

    PENDING = 'pending'
    STARTED = 'started'
    FINISHED = 'finished'
    STATUS_OPTIONS = (
        (PENDING, 'Pendiente'),
        (STARTED, 'Iniciado'),
        (FINISHED, 'Finalizado')
    )

    driver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='rides')
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=16, choices=STATUS_OPTIONS)
