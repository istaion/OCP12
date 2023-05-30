from django.contrib import admin
from django.urls import path, include
from app.views import UserRegistrationView, ClientView, ClientUniqueView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('registrate/', UserRegistrationView.as_view({'post': 'create'})),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('client/', ClientView.as_view({'post': 'create', 'get': 'list'})),
    path('client/<client_id>/', ClientUniqueView.as_view({'get': 'list', 'put': 'update', 'delete': 'delete'})),
    path('admin/', admin.site.urls),
]