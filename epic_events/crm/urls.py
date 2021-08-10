from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_jwt.views import obtain_jwt_token
from .views import *

clients_router = routers.SimpleRouter(trailing_slash=False)
clients_router.register(r"client/?", ClientViewSet)

contracts_router = routers.SimpleRouter(trailing_slash=False)
contracts_router.register(r"contract/?", ContractViewSet)

events_router = routers.SimpleRouter(trailing_slash=False)
events_router.register(r"event/?", EventViewSet)

urlpatterns = [
    path("", include(clients_router.urls)),
    path("", include(contracts_router.urls)),
    path("", include(events_router.urls)),
    path("login", obtain_jwt_token),
]
