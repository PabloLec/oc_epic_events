from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRole(models.Model):
    _possible_roles = [("management", "Management"), ("sales", "Sales"), ("support", "Support")]

    value = models.CharField(max_length=25, choices=_possible_roles, unique=True)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, role, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        management_role = UserRole.objects.filter(value="management")
        if not management_role.exists():
            raise Exception("Management role does not exists, run manage.py setup")
        role = management_role.first()

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, role, **extra_fields)


class User(AbstractUser):
    # TODO: Implémenter les methodes de admin panel pour que staff = is_admin)
    role = models.ForeignKey(to=UserRole, on_delete=models.RESTRICT)
    objects = UserManager()


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    company_name = models.CharField(max_length=25)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)


class ContractStatus(models.Model):
    _possible_status = [("ongoing", "Ongoing"), ("finished", "Finished")]
    value = models.CharField(max_length=25, choices=_possible_status, unique=True)


class Contract(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    # TODO Utiliser limit_choices_to=... pour n'afficher que les sales
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(to=ContractStatus, on_delete=models.RESTRICT)
    amount = models.IntegerField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="support_contact")
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name="sales_contact")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = None
    attendees = models.IntegerField()
    notes = models.TextField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        management = Group.objects.get(name="management")

        print(instance.role.value)

        if instance.role.value == "management":
            instance.is_staff = True
            instance.groups.add(management)
        else:
            instance.is_staff = False
            instance.groups.remove(management)
        instance.save()
