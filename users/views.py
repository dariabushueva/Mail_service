import string
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm, LoginForm
from users.models import User
from users.services import send_verification_email


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        verification_key = self.object.verification_key
        verification_url = self.request.build_absolute_uri(reverse("users:verify_email",
                                                                   kwargs={"key": verification_key}))
        send_verification_email(self.object.email, verification_url)
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, key):
    user = get_object_or_404(User, verification_key=key)
    user.is_active = True
    user.verification_key = ''
    user.save()
    return redirect('users:login')


@login_required
def generate_and_send_password(request):
    new_password = ''.join(random.sample(string.ascii_letters, 20))
    send_mail(
        subject='Новый пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('users:login'))


