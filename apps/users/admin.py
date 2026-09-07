from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'batch_name', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'batch_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Django Kalari Custom Fields', {'fields': ('role', 'batch_name', 'avatar_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Django Kalari Custom Fields', {'fields': ('role', 'batch_name', 'avatar_url')}),
    )
