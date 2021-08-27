from rest_framework import permissions

from .models import *


class IsInManagementTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.value == "management"


class IsClientSalesContact(permissions.BasePermission):
    def has_permission(self, request, view):
        is_sales = request.user.role.pk == get_role_id_by_name(name="sales")
        if "pk" not in view.kwargs:
            return request.method in ["GET", "POST"] and is_sales
        client = Client.objects.get(pk=view.kwargs["pk"])
        return client.sales_contact == request.user


class IsContractSalesContact(permissions.BasePermission):
    def has_permission(self, request, view):
        is_sales = request.user.role.pk == get_role_id_by_name(name="sales")
        if "pk" not in view.kwargs:
            return request.method in ["GET", "POST"] and is_sales
        contract = Contract.objects.get(pk=view.kwargs["pk"])
        return contract.client.sales_contact == request.user


class IsEventSalesContact(permissions.BasePermission):
    def has_permission(self, request, view):
        is_sales = request.user.role.pk == get_role_id_by_name(name="sales")
        if "pk" not in view.kwargs:
            return request.method in ["GET", "POST"] and is_sales
        event = Event.objects.get(pk=view.kwargs["pk"])
        return event.contract.client.sales_contact == request.user


class IsSupportContact(permissions.BasePermission):
    def has_permission(self, request, view):
        is_support = request.user.role.pk == get_role_id_by_name(name="support")
        if "pk" not in view.kwargs:
            return request.method == "GET" and is_support
        event = Event.objects.get(pk=view.kwargs["pk"])
        return event.support_contact == request.user
