from custom import BaseSerializer
from users.models import User, Vehicle

class UserSerializer(BaseSerializer):
    # Serializer for the User model

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "last_login", "is_superuser", "is_staff",
                  "is_active", "date_joined", "created_at", "role", "rating", "rating_count")


class VehicleSerializer(BaseSerializer):

    class Meta:
        model = Vehicle
        fields = ("id", "brand", "model", "seats", "color", "plate", "owner")