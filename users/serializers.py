from custom import BaseSerializer
from users.models import User

class UserSerializer(BaseSerializer):
    # Serializer for the User model

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "last_login", "is_superuser", "is_staff",
                  "is_active", "date_joined", "created_at", "role", "rating", "rating_count")
