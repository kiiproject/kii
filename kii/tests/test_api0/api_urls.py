from django.conf.urls import patterns, url, include
from .. import views

urlpatterns = patterns('',
    url(r'^hello', views.blank, name='index'),
)
