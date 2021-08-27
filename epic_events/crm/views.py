from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from .permissions import *


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filterset_fields = ("first_name", "last_name", "email")
    permission_classes = (IsInManagementTeam | IsInSalesTeam,)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filterset_fields = ("client__first_name", "client__last_name", "client__email", "created_time", "amount")
    permission_classes = (IsInManagementTeam | IsInSalesTeam,)


class EventViewSet(viewsets.ModelViewSet):
    def list(self, request):
        is_support = request.user.role.pk == get_role_id_by_name(name="support")
        if is_support:
            queryset = Event.objects.filter(support_contact=request.user)
        else:
            queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filterset_fields = ("client__first_name", "client__last_name", "client__email", "event_date")
    permission_classes = (IsInManagementTeam | IsInSalesTeam | IsSupportContact,)
