from django.contrib import admin
from game.models import DeployedTaskImage

@admin.register(DeployedTaskImage)
class DeployedTaskImageAdmin(admin.ModelAdmin):
    pass
