from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdminModel(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'is_active', 'username', 'email')
