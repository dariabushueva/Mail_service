from django.contrib import admin

from mailings.models import Mailing, Client, MailingSettings, MailingLogs


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('topic', 'slug',)
    search_fields = ('topic', 'body',)
    prepopulated_fields = {'slug': ('topic',)}


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'frequency', 'status')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('last_attempt', 'attempt_status', 'mailing_list')
