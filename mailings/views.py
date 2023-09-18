import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from mailings.forms import MailingForm, ClientForm
from mailings.models import Mailing, Client, MailingLogs


class Index(ListView):
    """ Главная страница """
    model = Blog
    template_name = 'mailings/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Blog.objects.filter(is_published=True)
        all_blogs = list(queryset)
        random_blogs = random.sample(all_blogs, 3)
        return random_blogs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        all_mailings = len(Mailing.objects.all())
        context_data['all_mailings'] = all_mailings
        active_mailings = len(Mailing.objects.filter(status=Mailing.LAUNCHED))
        context_data['active_mailings'] = active_mailings
        all_clients = len(Client.objects.all())
        context_data['all_clients'] = all_clients
        return context_data


class MailingListView(LoginRequiredMixin, ListView):
    """ Список рассылок """
    model = Mailing

    def get_queryset(self):
        if not self.request.user.is_staff:
            queryset = Mailing.objects.filter(owner=self.request.user).order_by('-pk')
        else:
            queryset = Mailing.objects.order_by('-pk')
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """ Детали определенной рассылки """
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    """ Создание рассылки """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование рассылки """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление рассылки  """
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Создание клиента """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """ Список клиентов """
    model = Client

    def get_queryset(self):
        if not self.request.user.is_staff:
            queryset = Client.objects.filter(owner=self.request.user)
        else:
            queryset = Client.objects.all()
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Детали определенного клиента """
    model = Client


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование клиента """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление клиента """
    model = Client
    success_url = reverse_lazy('mailings:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class MailingLogsListView(LoginRequiredMixin, ListView):
    """ Логи рассылки """
    model = MailingLogs

