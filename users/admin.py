from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'first_name', 'last_name', 'is_active')

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('mailings.set_status') and not request.user.is_superuser:
            user_fields = [field.name for field in User._meta.fields]
            user_fields += ['groups', 'user_permissions']
            user_fields.remove('is_active')
            return user_fields
        return self.readonly_fields
