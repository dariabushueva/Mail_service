from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.verification_key:
            user.verification_key = get_random_string(length=20)
        if commit:
            user.save()
        return user
