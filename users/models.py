from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):

    ADMIN = 'admin'
    USER = 'user'
    DRIVER = 'driver'

    ROLES = (
        (ADMIN, "Administrador"),
        (USER, "Usuario"),
        (DRIVER, "Conductor")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=16, choices=ROLES)
    rating = models.FloatField(default=5.0)
    rating_count = models.IntegerField(default=0)
    phone_number_area_code = models.CharField(max_length=4, default='')
    phone_number = models.CharField(max_length=7, default='')

    def __str__(self):
        return self.username
    

class Vehicle(models.Model):
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    seats = models.IntegerField(default=2)
    color = models.CharField(max_length=32)
    plate = models.CharField(max_length=8)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")