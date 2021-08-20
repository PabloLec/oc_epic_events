from rest_framework import viewsets
from .serializers import *
from .models import *
from .permissions import *


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsInManagementTeam | IsInSalesTeam,)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsInManagementTeam | IsInSalesTeam,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsInManagementTeam | IsInSalesTeam | IsSupportContact,)
