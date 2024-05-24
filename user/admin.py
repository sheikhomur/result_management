from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount


class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'email', 'full_name', 'is_staff', 'is_active')
    ordering = ['-date_joined']

    def full_name(self, obj):
        return obj.get_full_name()


admin.site.register(UserAccount, UserAccountAdmin)
