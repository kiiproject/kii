from django.conf.urls import patterns, url, include
from .. import views


urlpatterns = patterns('',
     url(r'^some_view', views.blank, name='some_view'),
)
