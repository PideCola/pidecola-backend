from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        )

    def validate(self, attrs):
        email = attrs["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "El usuario ya existe"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["email"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
