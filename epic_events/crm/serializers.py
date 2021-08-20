from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mobile",
            "company_name",
            "sales_contact",
        )


class ContractSerializer(serializers.ModelSerializer):
    payment_due_date = serializers.DateTimeField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])

    class Meta:
        model = Contract
        fields = (
            "id",
            "client",
            "amount",
            "payment_due_date",
            "sales_contact",
            "is_finished",
            "is_paid",
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "client",
            "contract",
            "attendees",
            "notes",
            "is_finished",
            "support_contact",
            "sales_contact",
        )
