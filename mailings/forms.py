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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['client'].queryset = Client.objects.filter(owner=self.user)
        if self.user.has_perm('mailings.set_status') and not self.user.is_superuser:
            for field_name, field in self.fields.items():
                if field_name != 'status':
                    field.widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.user.has_perm('mailings.set_status'):
            for field_name in self.fields:
                if self.fields[field_name].widget.attrs.get('readonly'):
                    cleaned_data.pop(field_name, None)
        return cleaned_data

    class Meta:
        model = Mailing
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    """ Форма клиента """

    class Meta:
        model = Client
        exclude = ('owner',)
