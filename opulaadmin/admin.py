from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = AuthenticationModel
    list_display = ('email','first_name', 'last_name', 'am_role', 'is_staff', 'am_is_deleted', 'am_created_at', 'am_updated_at')
    list_filter = ('is_staff', 'am_is_deleted', 'am_role__rm_role')  

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password', 'am_role')}),
        ('Permissions', {'fields': ('is_staff', 'am_is_deleted')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name', 'last_name', 'password1', 'password2', 'am_role', 'is_staff', 'am_is_deleted')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_role(self, obj):
        return obj.am_role.rm_role if obj.am_role else 'No Role'
    get_role.short_description = 'Role'  

admin.site.register(AuthenticationModel, CustomUserAdmin)


















