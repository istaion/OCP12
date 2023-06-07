from rest_framework.permissions import BasePermission
from .models import Client, Contract


class HasClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "support":
            return request.method == "GET"
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            if request.user.role == "support":
                return obj in Client.objects.filter(
                    contract__event__support=request.user
                )
            else:
                return True
        else:
            return request.user == obj.sales
