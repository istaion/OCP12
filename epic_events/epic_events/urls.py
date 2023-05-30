from django.contrib import admin
from django.urls import path, include
from app.views import UserRegistrationView, ClientView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('registrate/', UserRegistrationView.as_view({'post': 'create'})),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/', ClientView.as_view({'post': 'create', 'get': 'list'})),
    path('admin/', admin.site.urls),
]