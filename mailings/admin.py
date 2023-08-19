from django.contrib import admin

from mailings.models import Mailing, Client,  MailingLogs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'topic', 'status', 'start_time', 'frequency',)
    list_filter = ('status',)
    search_fields = ('topic', 'body',)
    prepopulated_fields = {'slug': ('topic',)}


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'attempt_status', 'mailing',)
