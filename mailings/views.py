from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.models import Mailing, Client, MailingLogs
from mailings.services import send_mailings


def index(request):
    return render(request, 'mailings/index.html')


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = Mailing.objects.order_by('-pk')
        return queryset


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('topic', 'body', 'slug', 'status', 'start_time', 'frequency', 'client',)
    success_url = reverse_lazy('mailings:mailing_list')

  #  def form_valid(self, form):
  #      obj = form.save()
  #      send_mailings(obj)
  #      return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('topic', 'body', 'slug', 'status', 'start_time', 'frequency', 'client',)
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'name', 'comment',)
    success_url = reverse_lazy('mailings:mailing_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'name', 'comment')
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class MailingLogsListView(ListView):
    model = MailingLogs

