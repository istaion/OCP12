from django.contrib import admin
from django.urls import path, include
from app.views import (
    UserRegistrationView,
    ClientView,
    ContractsView,
    EventsView,
    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter, SimpleRouter

router = DefaultRouter()
router.register("client", ClientView, basename="client")
router.register("contract", ContractsView, basename="contract")
router.register("event", EventsView, basename="event")

urlpatterns = [
    path('registrate/', UserRegistrationView.as_view({'post': 'create'})),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]