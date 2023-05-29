from django.contrib import admin
from django.urls import path, include
from app.views import UserRegistrationView


urlpatterns = [
    path('registrate/', UserRegistrationView.as_view({'post': 'create'})),
    path('admin/', admin.site.urls),
]