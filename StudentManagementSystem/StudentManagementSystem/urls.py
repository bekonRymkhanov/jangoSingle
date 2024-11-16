from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView  # Import blacklist view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('auth/jwt/blacklist/', TokenBlacklistView.as_view(), name='jwt-blacklist'), 
    path('', include('grades.urls')),
    path('', include('attendance.urls')),
    path('', include('students.urls')),
    path('', include('courses.urls')),
    path('', include('users.urls')),
    path('', include('notifications.urls')),
]
