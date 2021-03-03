from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User, Role, Permission


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'mobile', 'is_active', 'is_staff',
        'create_time', 'update_time'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # fields = ('username', 'email')
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'mobile', 'roles', 'is_active', 'is_staff')
        }),
    )
    filter_horizontal = ('roles',)


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
