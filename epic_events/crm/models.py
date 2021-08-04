from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserRole(models.Model):
    def __str__(self):
        return f"{self.value}"

    _possible_roles = [("management", "Management"), ("sales", "Sales"), ("support", "Support")]

    value = models.CharField(max_length=25, choices=_possible_roles, unique=True)


def get_role_id_by_name(name: str):
    for id_num, role in enumerate(UserRole._possible_roles, start=1):
        if role[0] == name:
            return id_num


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
    def __str__(self):
        return f"{self.username}"

    role = models.ForeignKey(to=UserRole, on_delete=models.RESTRICT)
    objects = UserManager()


class Client(models.Model):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    first_name = models.CharField(max_length=25, verbose_name="Prénom")
    last_name = models.CharField(max_length=25, verbose_name="Nom")
    email = models.EmailField()
    phone = models.CharField(max_length=10, verbose_name="Téléphone")
    mobile = models.CharField(max_length=10, verbose_name="Mobile")
    company_name = models.CharField(max_length=25, verbose_name="Nom de l'entreprise")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    sales_contact = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": get_role_id_by_name(name="sales")},
        verbose_name="Contact Vente",
    )


class Contract(models.Model):
    def __str__(self):
        return f"{self.client} -  {self.created_time.strftime('%d/%m/%Y - %H:%M:%S')}"

    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": get_role_id_by_name(name="sales")},
        verbose_name="Contact Vente",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    is_finished = models.BooleanField(default=False, verbose_name="Est terminé")
    is_paid = models.BooleanField(default=False, verbose_name="Est payé")
    amount = models.IntegerField(verbose_name="Montant")
    payment_due_date = models.DateTimeField(verbose_name="Echéance du paiement")


class Event(models.Model):
    def __str__(self):
        return f"{self.client} -  {self.created_time.strftime('%d/%m/%Y - %H:%M:%S')}"

    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE, verbose_name="Contrat")
    support_contact = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="support_contact",
        limit_choices_to={"role": get_role_id_by_name(name="support")},
        verbose_name="Contact Support",
    )
    sales_contact = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sales_contact",
        limit_choices_to={"role": get_role_id_by_name(name="sales")},
        verbose_name="Contact Vente",
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    is_finished = models.BooleanField(default=False, verbose_name="Est terminé")
    attendees = models.IntegerField(verbose_name="Participants")
    notes = models.TextField()


@receiver(post_save, sender=User)
def handle_management_role(sender, instance, created, **kwargs):
    if created:
        management = Group.objects.get(name="management")

        if instance.role.value == "management":
            instance.is_staff = True
            instance.groups.add(management)
        else:
            instance.is_staff = False
            instance.groups.remove(management)
        instance.save()
