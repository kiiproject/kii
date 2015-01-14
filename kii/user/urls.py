from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^login$', views.login, name="login"), # NOQA
    url(r'^logout$', views.logout, {'next_page': '/'}, name="logout"),
)
