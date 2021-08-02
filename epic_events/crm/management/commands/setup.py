from crm import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def create_user_roles(self):
        for value, name in models.UserRole._possible_roles:
            if not models.UserRole.objects.filter(value=value).exists():
                print(" - Creating user role:", value)
                models.UserRole.objects.create(value=value)
        print(" - User roles created")

    def create_management_group(self):
        accessible_models = ("client", "contract", "event", "user")
        permissions = ("add", "change", "view", "delete")
        group, created = Group.objects.get_or_create(name="management")

        for model in accessible_models:
            for permission in permissions:
                name = f"Can {permission} {model}"
                print(f"Creating {name}")

                try:
                    model_add_perm = Permission.objects.get(name=name)
                except Permission.DoesNotExist:
                    print(" ! Error with permission:", name)
                    continue

                group.permissions.add(model_add_perm)

    def handle(self, *args, **options):
        self.create_user_roles()
        self.create_management_group()
