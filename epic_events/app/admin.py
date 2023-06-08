from django.contrib import admin
from .models import CustomUser, Client, Contract, Event


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ("email", "role", "id")


class ClientAdmin(admin.ModelAdmin):

    list_display = ("id", "existing", "sales")


class ContractAdmin(admin.ModelAdmin):

    list_display = ("id", "signed", "client", "sales")


class EventAdmin(admin.ModelAdmin):

    list_display = ("id", "contract", "support")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)


