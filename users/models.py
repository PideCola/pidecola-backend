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

    def __str__(self):
        return self.username