from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin
from .models import *

from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email", "role", "is_active")

    def clean(self):
        if self.cleaned_data.get("role") is None:
            pass
        elif self.cleaned_data.get("role").value == "management":
            self.cleaned_data["is_staff"] = True
            self.cleaned_data["groups"] = Group.objects.filter(name="management")
        else:
            self.cleaned_data["is_staff"] = False
            self.cleaned_data["groups"] = Group.objects.none()

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser and db_field.name == "role":
            kwargs["queryset"] = UserRole.objects.filter(value="sales") | UserRole.objects.filter(value="support")
        return super(UserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    form = UserForm

    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role",)

    search_fields = ("username__startswith",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "sales_contact",
        "created_time",
    )
    list_filter = ("sales_contact",)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "sales_contact",
        "client",
        "created_time",
    )
    list_filter = (
        "client",
        "sales_contact",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "sales_contact",
        "support_contact",
        "client",
        "contract",
        "created_time",
    )
    list_filter = (
        "client",
        "sales_contact",
        "support_contact",
    )
