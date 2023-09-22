from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'phone', 'first_name', 'last_name', 'is_active')
    list_display_links = ('pk', 'email',)

