from django.contrib import admin

from clients.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


admin.site.register(Client, ClientAdmin)
