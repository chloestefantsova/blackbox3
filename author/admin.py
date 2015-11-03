from django.contrib import admin
from author.models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    pass

