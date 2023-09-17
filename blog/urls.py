from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('view/<slug>/', BlogDetailView.as_view(), name='blog_view'),
    path('edit/<slug>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('delete/<slug>', BlogDeleteView.as_view(), name='blog_delete')
]
