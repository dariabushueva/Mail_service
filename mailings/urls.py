from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingListView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list')
]
