from rest_framework import permissions

from .models import *


class IsInManagementTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.value == "management"


class IsInSalesTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.role.value == "sales")
        return request.user.role.value == "sales"


class IsSupportContact(permissions.BasePermission):
    def has_permission(self, request, view):
        event = Event.objects.get(pk=view.kwargs["pk"])
        return event.support_contact == request.user
