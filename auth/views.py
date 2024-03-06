from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from auth.serializers import RegisterSerializer

User = get_user_model()


# Create your views here.
class RegisterView(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(access)
        return Response(
            {
                "message": "User registered successfully!",
                "access": access_token,
                "refresh": refresh_token,
            },
            status=status.HTTP_201_CREATED,
        )
