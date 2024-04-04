from custom import BaseSerializer
from users.models import User, Vehicle, HonorificTitle

class HonorificTitleSerializer(BaseSerializer):
    class Meta:
        model = HonorificTitle
        fields = "__all__"

class UserSerializer(BaseSerializer):
    honorific_titles = HonorificTitleSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "last_login", "is_superuser", "is_staff",
                  "is_active", "date_joined", "created_at", "role", "likes", "dislikes", "phone_number", "honorific_titles")


class VehicleSerializer(BaseSerializer):

    class Meta:
        model = Vehicle
        fields = ("id", "brand", "model", "seats", "color", "plate", "owner")