from django.conf.urls import patterns, include, url
from . import views
urlpatterns = patterns('',

    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    
) 
