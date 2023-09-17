from django.contrib import admin

from mailings.models import Mailing, Client,  MailingLogs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'topic', 'status', 'owner', 'start_time', 'frequency',)
    list_display_links = ('pk', 'topic',)
    list_filter = ('status', 'owner',)
    search_fields = ('topic', 'body',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('mailings.set_status') and not request.user.is_superuser:
            return ['topic', 'body', 'slug', 'start_time', 'frequency', 'client', 'owner']
        return self.readonly_fields


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'owner',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'attempt_status', 'mailing',)
