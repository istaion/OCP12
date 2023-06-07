from django.contrib import admin
from .models import CustomUser, Client, Contract, Event


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ("email", "role", "id")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)


