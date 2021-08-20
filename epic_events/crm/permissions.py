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
        is_support = request.user.role.pk == get_role_id_by_name(name="support")
        if "pk" not in view.kwargs:
            return request.method == "GET" and is_support
        event = Event.objects.get(pk=view.kwargs["pk"])
        return event.support_contact == request.user
