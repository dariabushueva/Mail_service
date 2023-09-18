from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from .views import *

app_name = MailingsConfig.name

urlpatterns = [
    path('', cache_page(360)(Index.as_view()), name='index'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<slug:slug>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_edit/<slug:slug>', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing_delete/<slug:slug>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('logs_list/', MailingLogsListView.as_view(), name='logs_list')
]
