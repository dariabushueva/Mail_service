from django import forms

from blog.models import Blog
from mailings.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """ Форма записи блога """

    class Meta:
        model = Blog
        exclude = ('is_published', 'count_views',)
