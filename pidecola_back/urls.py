"""
URL configuration for pidecola_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from auth.views import RegisterView
from users.urls import router as users_router
from rides.urls import router as rides_router

main_router = DefaultRouter()
main_router.registry.extend(users_router.registry)
main_router.registry.extend(rides_router.registry)

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/register/', RegisterView.as_view({'post': 'create'}), name='auth_register'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/v1/', include(main_router.urls)),
    # path("api_schema/", get_schema_view(
    #         title="Pidecola 3.1", description="", version="1.0.0"
    #         ),
    #     name="openapi-schema",
    # ),
]
