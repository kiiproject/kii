from django.conf.urls import patterns, url, include
from .. import views
from django.views.generic import TemplateView
from .views import Home

urlpatterns = patterns('',
    url(r'^hello', views.blank, name='index'),
    url(r'^hello/first', views.blank, name='first'),
    url(r'^hello/second', views.blank, name='second'),
    url(r'^hello/third', views.blank, name='third'),
    url(r'^hello/user', views.blank, name='user'),
    url(r'^home', Home.as_view(template_name="test_app/home.html"), name='home'),
)
