from django.conf.urls import patterns, url, include
from .. import views


urlpatterns = patterns('',
     url(r'^third_view', views.blank, name='third_view'),
)
