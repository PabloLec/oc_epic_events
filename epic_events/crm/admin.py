from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Contract)
admin.site.register(Client)
admin.site.register(Event)


# Créer les méthodes admin https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
