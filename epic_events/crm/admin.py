from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .models import *

from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'role', 'is_active')

    def clean(self):
        if self.cleaned_data.get('role') is None:
            pass
        elif self.cleaned_data.get('role').value == "management":
            self.cleaned_data['is_staff']  = True
            self.cleaned_data['groups'] = Group.objects.filter(name="management")
        else:
            self.cleaned_data['is_staff']  = False
            self.cleaned_data['groups'] = Group.objects.none()

        return self.cleaned_data

    def save(self, commit=True):
            # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdminCustom(admin.ModelAdmin):
    form = UserForm

    list_display = ("username", "email","role", "is_staff")
    list_filter = ("role",)

    search_fields = ("username__startswith", )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("__str__","sales_contact","created_time",)
    list_filter = ("sales_contact",)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("__str__","sales_contact","client","created_time",)
    list_filter = ("client","sales_contact",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("__str__","sales_contact","support_contact","client","contract","created_time",)
    list_filter = ("client","sales_contact","support_contact",)

admin.site.unregister(Group)


class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0


@admin.register(Group)
class GenericGroup(GroupAdmin):
    inlines = [UserInLine]

