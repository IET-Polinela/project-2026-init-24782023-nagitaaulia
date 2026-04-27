from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff')
    list_filter = ('is_admin', 'is_member', 'is_staff')