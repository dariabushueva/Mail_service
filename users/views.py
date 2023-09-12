from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User
from users.services import send_verification_email


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


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


def verify_email(request, key):
    user = get_object_or_404(User, verification_key=key)
    user.is_active = True
    user.verification_key = ''
    user.save()
    return redirect('users:login')


