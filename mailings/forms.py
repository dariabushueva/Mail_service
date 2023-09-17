from django import forms

from mailings.models import Mailing, Client


class StyleFormMixin:
    """ Виджет для форм """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """ Форма рассылки """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['client'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Mailing
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    """ Форма клиента """

    class Meta:
        model = Client
        exclude = ('owner',)
